#!/usr/bin/env python3
"""
SINYFY v1.0 - ЛАЙТ ВЕРСИЯ
Static Site Visual Cloner (Без Selenium)
Автор: thetemirbolatov

Использование: python sinyfy.py https://example.com
"""

import os
import re
import sys
import json
import base64
import hashlib
import logging
import argparse
import requests
from urllib.parse import urljoin, urlparse
from datetime import datetime
from bs4 import BeautifulSoup, Comment, Doctype
from PIL import Image, ImageDraw, ImageFont

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sinyfy.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('SINYFY')

class Sinyfy:
    """Основной класс SINYFY (без Selenium)"""
    
    def __init__(self, url, output_dir="output", download_images=True):
        self.url = url
        self.output_dir = output_dir
        self.download_images = download_images
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Создание директорий
        self.images_dir = os.path.join(output_dir, 'images')
        os.makedirs(self.images_dir, exist_ok=True)
        
        self.image_counter = 1
        self.css_parts = []
        self.resources = []
        
    def fetch_page(self):
        """Загрузка HTML страницы"""
        logger.info(f"Загрузка: {self.url}")
        
        try:
            response = self.session.get(self.url, timeout=30)
            response.encoding = response.apparent_encoding or 'utf-8'
            response.raise_for_status()
            
            logger.info(f"Страница загружена: {len(response.text)} байт")
            return response.text
            
        except Exception as e:
            logger.error(f"Ошибка загрузки: {e}")
            raise
    
    def parse_html(self, html):
        """Парсинг HTML"""
        logger.info("Парсинг HTML...")
        
        self.soup = BeautifulSoup(html, 'html.parser')
        
        # Создание структуры при необходимости
        if not self.soup.html:
            self.soup.append(self.soup.new_tag('html'))
        if not self.soup.head:
            self.soup.html.insert(0, self.soup.new_tag('head'))
        if not self.soup.body:
            self.soup.html.append(self.soup.new_tag('body'))
    
    def extract_css(self):
        """Извлечение CSS"""
        logger.info("Извлечение CSS...")
        
        all_css = []
        
        # 1. Теги style
        for style in self.soup.find_all('style'):
            if style.string:
                css_text = self._clean_css(style.string)
                all_css.append(f"/* Из тега style */\n{css_text}")
                style.decompose()
        
        # 2. Внешние CSS файлы
        for link in self.soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                full_url = urljoin(self.url, href)
                css_text = self._download_css(full_url)
                if css_text:
                    all_css.append(f"/* Источник: {href} */\n{css_text}")
                link.decompose()
        
        # 3. Инлайн стили в классы
        self._extract_inline_styles()
        
        # Объединение CSS
        final_css = "\n\n".join(all_css)
        
        # Добавление сохраненных инлайн стилей
        if self.css_parts:
            final_css += "\n\n/* Инлайн стили */\n" + "\n".join(self.css_parts)
        
        logger.info(f"CSS извлечен: {len(all_css)} источников")
        return final_css
    
    def _clean_css(self, css_text):
        """Очистка CSS"""
        # Удаление комментариев
        css_text = re.sub(r'/\*.*?\*/', '', css_text, flags=re.DOTALL)
        # Удаление пустых правил
        css_text = re.sub(r'[^{]+\{\s*\}', '', css_text)
        return css_text
    
    def _download_css(self, url):
        """Загрузка CSS файла"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.debug(f"Не удалось загрузить CSS {url}: {e}")
            return None
    
    def _extract_inline_styles(self):
        """Извлечение инлайн стилей в классы"""
        style_counter = 1
        for tag in self.soup.find_all(style=True):
            style_text = tag['style']
            class_name = f'sinyfy-inline-{style_counter}'
            style_counter += 1
            
            # Добавление класса
            if tag.has_attr('class'):
                tag['class'].append(class_name)
            else:
                tag['class'] = [class_name]
            
            # Сохранение стиля
            self.css_parts.append(f".{class_name} {{\n  {style_text};\n}}")
            
            # Удаление атрибута style
            del tag['style']
    
    def process_images(self):
        """Обработка изображений"""
        if not self.download_images:
            logger.info("Пропуск изображений")
            return
        
        logger.info("Обработка изображений...")
        image_count = 0
        
        for img in self.soup.find_all('img'):
            src = img.get('src')
            if src:
                if self._process_image(src, img):
                    image_count += 1
        
        # Фоновые изображения
        self._process_background_images()
        
        logger.info(f"Обработано изображений: {image_count}")
    
    def _process_image(self, src, tag):
        """Обработка одного изображения"""
        try:
            # Data URI
            if src.startswith('data:'):
                return self._process_data_uri(src, tag)
            
            # Обычный URL
            full_url = urljoin(self.url, src)
            
            # Определение расширения
            ext = self._get_extension(full_url)
            filename = f"image_{self.image_counter:04d}{ext}"
            self.image_counter += 1
            
            local_path = os.path.join('images', filename)
            full_local_path = os.path.join(self.images_dir, filename)
            
            # Скачивание
            if self._download_file(full_url, full_local_path):
                tag['src'] = local_path
                self._add_image_dimensions(tag, full_local_path)
                
                self.resources.append({
                    'type': 'image',
                    'url': full_url,
                    'local': local_path,
                    'size': os.path.getsize(full_local_path)
                })
                return True
            else:
                return self._create_placeholder(tag)
                
        except Exception as e:
            logger.error(f"Ошибка обработки {src}: {e}")
            return self._create_placeholder(tag)
    
    def _process_data_uri(self, data_uri, tag):
        """Обработка data URI"""
        try:
            match = re.match(r'data:image/([^;]+);base64,(.+)', data_uri)
            if match:
                img_format, base64_data = match.groups()
                filename = f"image_data_{self.image_counter:04d}.{img_format}"
                self.image_counter += 1
                
                local_path = os.path.join('images', filename)
                full_local_path = os.path.join(self.images_dir, filename)
                
                # Декодирование
                img_data = base64.b64decode(base64_data)
                with open(full_local_path, 'wb') as f:
                    f.write(img_data)
                
                tag['src'] = local_path
                return True
        except:
            pass
        return False
    
    def _process_background_images(self):
        """Обработка фоновых изображений"""
        for tag in self.soup.find_all(style=True):
            style = tag['style']
            if 'background' in style:
                # Поиск URL
                urls = re.findall(r'url\([\'"]?([^\'")]+)[\'"]?\)', style)
                for url in urls:
                    if not url.startswith('data:'):
                        full_url = urljoin(self.url, url)
                        ext = self._get_extension(full_url)
                        filename = f"bg_{self.image_counter:04d}{ext}"
                        self.image_counter += 1
                        
                        local_path = os.path.join('images', filename)
                        full_local_path = os.path.join(self.images_dir, filename)
                        
                        if self._download_file(full_url, full_local_path):
                            style = style.replace(url, local_path)
                
                tag['style'] = style
    
    def _download_file(self, url, local_path):
        """Скачивание файла"""
        try:
            response = self.session.get(url, timeout=10, stream=True)
            response.raise_for_status()
            
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)
            return True
        except:
            return False
    
    def _create_placeholder(self, tag):
        """Создание заглушки"""
        filename = f"placeholder_{self.image_counter:04d}.png"
        self.image_counter += 1
        
        local_path = os.path.join('images', filename)
        full_local_path = os.path.join(self.images_dir, filename)
        
        # Создание PNG
        try:
            img = Image.new('RGB', (200, 150), color='#f0f0f0')
            draw = ImageDraw.Draw(img)
            
            # Рамка
            draw.rectangle([0, 0, 199, 149], outline='#cccccc', width=2)
            draw.line([0, 0, 200, 150], fill='#cccccc', width=1)
            draw.line([200, 0, 0, 150], fill='#cccccc', width=1)
            
            # Текст
            draw.text((70, 65), "NO IMAGE", fill='#666666')
            
            img.save(full_local_path, 'PNG')
        except:
            # Если PIL не работает, создаем пустой файл
            with open(full_local_path, 'wb') as f:
                f.write(b'')
        
        tag['src'] = local_path
        tag['data-sinyfy'] = 'placeholder'
        return True
    
    def _get_extension(self, url):
        """Получение расширения файла"""
        path = urlparse(url).path
        ext = os.path.splitext(path)[1].lower()
        
        valid_exts = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
        if ext in valid_exts:
            return ext
        return '.png'
    
    def _add_image_dimensions(self, tag, image_path):
        """Добавление размеров"""
        try:
            if os.path.exists(image_path):
                with Image.open(image_path) as img:
                    tag['width'] = str(img.width)
                    tag['height'] = str(img.height)
        except:
            pass
    
    def clean_html(self):
        """Очистка HTML"""
        logger.info("Очистка HTML...")
        
        # Удаление DOCTYPE
        for doctype in self.soup.find_all(string=lambda text: isinstance(text, Doctype)):
            doctype.extract()
        
        # Удаление комментариев
        for comment in self.soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()
        
        # Удаление скриптов
        for script in self.soup.find_all('script'):
            script.decompose()
        
        # Удаление обработчиков событий
        events = ['onclick', 'onload', 'onsubmit', 'onerror', 'onmouseover',
                  'onmouseout', 'onchange', 'onfocus', 'onblur']
        
        for tag in self.soup.find_all(True):
            for event in events:
                if tag.has_attr(event):
                    del tag[event]
            
            # Нормализация ссылок
            if tag.name == 'a' and tag.has_attr('href'):
                if tag['href'].startswith(('javascript:', '#', 'mailto:')):
                    tag['href'] = '#'
            
            if tag.name == 'form' and tag.has_attr('action'):
                tag['action'] = '#'
    
    def add_css_link(self):
        """Добавление ссылки на CSS"""
        head = self.soup.head
        
        # Удаление старых CSS ссылок
        for link in head.find_all('link', rel='stylesheet'):
            link.decompose()
        
        # Добавление новой
        css_link = self.soup.new_tag('link', rel='stylesheet', href='style.css')
        head.append(css_link)
        
        # Комментарий
        comment = Comment(f" SINYFY v1.0 by thetemirbolatov ")
        head.append(comment)
    
    def save_files(self, css_content):
        """Сохранение файлов"""
        logger.info("Сохранение файлов...")
        
        # HTML
        html_path = os.path.join(self.output_dir, 'index.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(str(self.soup.prettify()))
        logger.info(f"HTML: {html_path}")
        
        # CSS
        if css_content:
            css_path = os.path.join(self.output_dir, 'style.css')
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(css_content)
            logger.info(f"CSS: {css_path}")
        
        # Манифест
        manifest = {
            'generator': 'SINYFY v1.0',
            'author': 'thetemirbolatov',
            'url': self.url,
            'date': datetime.now().isoformat(),
            'resources': self.resources
        }
        
        manifest_path = os.path.join(self.output_dir, 'manifest.json')
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        logger.info(f"Манифест: {manifest_path}")
    
    def run(self):
        """Запуск"""
        try:
            logger.info("=" * 60)
            logger.info("SINYFY v1.0 (Лайт версия)")
            logger.info(f"Автор: thetemirbolatov")
            logger.info(f"URL: {self.url}")
            logger.info("=" * 60)
            
            # Загрузка страницы
            html = self.fetch_page()
            
            # Парсинг
            self.parse_html(html)
            
            # Извлечение CSS
            css_content = self.extract_css()
            
            # Обработка изображений
            self.process_images()
            
            # Очистка HTML
            self.clean_html()
            
            # Добавление CSS ссылки
            self.add_css_link()
            
            # Сохранение
            self.save_files(css_content)
            
            # Статистика
            logger.info("=" * 60)
            logger.info(f"ГОТОВО!")
            logger.info(f"Папка: {os.path.abspath(self.output_dir)}")
            logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            logger.error(f"ОШИБКА: {e}")
            if '--debug' in sys.argv:
                import traceback
                traceback.print_exc()
            return False

def main():
    """Точка входа"""
    parser = argparse.ArgumentParser(description='SINYFY v1.0 - Клонер сайтов')
    parser.add_argument('url', help='URL сайта')
    parser.add_argument('-o', '--output', default='output', help='Папка для сохранения')
    parser.add_argument('--no-images', action='store_true', help='Не скачивать изображения')
    parser.add_argument('--debug', action='store_true', help='Режим отладки')
    
    args = parser.parse_args()
    
    # Запуск
    cloner = Sinyfy(
        url=args.url,
        output_dir=args.output,
        download_images=not args.no_images
    )
    
    success = cloner.run()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()