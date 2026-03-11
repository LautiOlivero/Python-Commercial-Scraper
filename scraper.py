import os
import random
import pandas as pd
from playwright.sync_api import sync_playwright
from config import USER_AGENTS, SELECTORS, EXPORT_FILE, BACKUP_FILE

def extract_data(url: str) -> dict:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        user_agent = random.choice(USER_AGENTS)
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()
        
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            data = {"url": url, "title": "Sin título", "price": "N/A", "stock": "N/A"}
            
            for key, selector in SELECTORS.items():
                element = page.locator(selector).first
                if element.count() > 0:
                    data[key] = element.inner_text().strip()
                    
            df = pd.DataFrame([data])
            
            for file in [EXPORT_FILE, BACKUP_FILE]:
                file_exists = os.path.isfile(file)
                try:
                    df.to_csv(file, mode='a', header=not file_exists, index=False)
                except PermissionError:
                    if file == EXPORT_FILE:
                        raise PermissionError(f"No se puede escribir en '{file}'. Asegúrese de que el archivo no esté abierto en otro programa.")
            
            return data
            
        finally:
            browser.close()
