USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
]

SELECTORS = {
    "title": "h1, .product-title, .product-name",
    "price": ".price, .product-price, .price_color, [data-price]",
    "stock": ".stock, .availability, [data-stock]"
}


EXPORT_FILE = "exportacion_datos.csv"
BACKUP_FILE = "historial_completo.csv"
