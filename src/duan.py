import sys
import requests
from bs4 import BeautifulSoup
import random
import time
from fake_useragent import UserAgent

# Đảm bảo sử dụng UTF-8 cho output
sys.stdout.reconfigure(encoding='utf-8')

# Tạo đối tượng User-Agent ngẫu nhiên để tránh bị chặn IP
ua = UserAgent()

# Hàm lấy giá sản phẩm từ Shopee
def get_shopee_price(url):
    headers = {
        "User-Agent": ua.random,  # Sử dụng User-Agent ngẫu nhiên
    }

    try:
        # Gửi yêu cầu GET tới URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Kiểm tra xem yêu cầu có thành công không (mã trạng thái 200)

        # Phân tích nội dung HTML của trang
        soup = BeautifulSoup(response.content, 'html.parser')

        # Sử dụng selector mới cho Shopee
        price_tag = soup.find('div', {'class': 'IZPeQz B67UQ0'})  # Class mới của Shopee
   
        if price_tag:
            price = price_tag.get_text()
            return price
        else:
            return "Không tìm thấy giá trên Shopee."

    except requests.exceptions.RequestException as e:
        return f"Đã xảy ra lỗi khi lấy dữ liệu từ Shopee: {e}"

# Hàm lấy giá sản phẩm từ Lazada
def get_lazada_price(url):
    headers = {
        "User-Agent": ua.random,  # Sử dụng User-Agent ngẫu nhiên
    }

    try:
        # Gửi yêu cầu GET tới URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Kiểm tra xem yêu cầu có thành công không (mã trạng thái 200)

        # Phân tích nội dung HTML của trang
        soup = BeautifulSoup(response.content, 'html.parser')
 
        # Sử dụng selector mới cho Lazada
        price_tag = soup.find('span', {'class': 'notranslate pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl'})  # Class mới của Lazada
    
        if price_tag:
            price = price_tag.get_text()
            return price
        else :return "Không tìm thấy giá trên Lazada."

    except requests.exceptions.RequestException as e:
        return f"Đã xảy ra lỗi khi lấy dữ liệu từ Lazada: {e}"

# Hàm xử lý việc lấy giá từ cả 2 trang
def get_price_from_ecommerce(url, platform):
    if platform.lower() == 'https://shopee.vn/':
        return get_shopee_price(url)
    elif platform.lower() == 'https://www.lazada.vn/#?':
        return get_lazada_price(url)
    else:
        return "Nền tảng không hợp lệ. Vui lòng chọn 'Shopee' hoặc 'Lazada'."


# Ví dụ sử dụng ứng dụng:
if __name__ == "__main__":
    # URL của sản phẩm trên Shopee và Lazada
    shopee_url = 'https://shopee.vn/Ch%C6%A1i-Video-USB-C-HUB-3.0-Lo%E1%BA%A1i-C-3.1-3-C%E1%BB%95ng-%C4%90a-USB-Splitter-B%E1%BB%99-Chuy%E1%BB%83n-%C4%90%E1%BB%95iOTG-Cho-Xiaomi-Lenovo-Macbook-Pro-13-15-Air-Pro-Ph%E1%BB%A5-Ki%E1%BB%87n-M%C3%A1y-T%C3%ADnh-i.196261835.29210818532'  # Thay thế bằng URL thực tế
    lazada_url = 'https://www.lazada.vn/products/sua-rua-mat-kiem-soat-nhon-ngan-ngua-mun-dang-gel-acnes-oil-control-cleanser-100g-i1216340-s1509483.html?scm=1007.17760.398138.0&pvid=64f76eef-0a00-4279-ba04-e2d1122ef056&search=flashsale&spm=a2o4n.homepage.FlashSale.d_1216340'  # Thay thế bằng URL thực tế
   
    # Lấy giá từ Shopee
    shopee_price = get_price_from_ecommerce(shopee_url, 'https://shopee.vn/')
    print(f"Giá sản phẩm trên Shopee: {shopee_price}")

    # Lấy giá từ Lazada
    lazada_price = get_price_from_ecommerce(lazada_url, 'https://www.lazada.vn/#?')
    print(f"Giá sản phẩm trên Lazada: {lazada_price}")

    # Để tránh bị chặn IP, ta có thể thêm một khoảng thời gian chờ giữa các yêu cầu:
    time.sleep(random.randint(2, 5))  # Thời gian chờ ngẫu nhiên từ 2 đến 5 giây
