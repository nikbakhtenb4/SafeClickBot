# create clicker robot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random


class SafeClickBot:
    def __init__(self, headless=False):
        """
        ایجاد ربات کلیک امن
        headless: اگر True باشه، مرورگر پنهان اجرا میشه
        """
        # تنظیمات مرورگر
        self.options = Options()
        if headless:
            self.options.add_argument("--headless")

        # تنظیمات ضد تشخیص
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )

        # ایجاد درایور
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        # تنظیم timeout
        self.wait = WebDriverWait(self.driver, 10)

        # نقاط مجاز برای کلیک (CSS Selector یا XPath)
        self.allowed_click_points = {
            "buy_button": "button[id*='buy']",
            "sell_button": "button[id*='sell']",
            "refresh_button": "button[class*='refresh']",
            "portfolio_tab": "a[href*='portfolio']",
            "market_tab": "a[href*='market']",
        }

        # لاگ فعالیت‌ها
        self.activity_log = []

    def human_delay(self, min_seconds=1, max_seconds=3):
        """تاخیر تصادفی برای شبیه‌سازی انسان"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        return delay

    def natural_mouse_movement(self, element):
        """حرکت طبیعی موس به سمت المان"""
        actions = ActionChains(self.driver)
        # حرکت به نقطه‌ای نزدیک المان
        actions.move_to_element_with_offset(
            element, random.randint(-5, 5), random.randint(-5, 5)
        )
        actions.perform()
        self.human_delay(0.2, 0.8)

        # حرکت دقیق به المان
        actions.move_to_element(element)
        actions.perform()
        self.human_delay(0.1, 0.3)

    def safe_click(self, point_name, wait_for_load=True):
        """
        کلیک امن روی نقاط مجاز
        point_name: نام نقطه از لیست allowed_click_points
        wait_for_load: منتظر بمانه صفحه لود شود
        """
        if point_name not in self.allowed_click_points:
            print(f"خطا: نقطه '{point_name}' در لیست مجاز نیست!")
            return False

        try:
            # پیدا کردن المان
            selector = self.allowed_click_points[point_name]
            element = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )

            # بررسی قابل مشاهده بودن
            if not element.is_displayed():
                print(f"المان '{point_name}' قابل مشاهده نیست!")
                return False

            # حرکت طبیعی موس
            self.natural_mouse_movement(element)

            # کلیک
            element.click()

            # ثبت در لاگ
            self.activity_log.append(
                {
                    "action": "click",
                    "target": point_name,
                    "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "success": True,
                }
            )

            print(f"✓ کلیک موفق روی '{point_name}'")

            # تاخیر بعد کلیک
            if wait_for_load:
                self.human_delay(2, 4)

            return True

        except Exception as e:
            print(f"خطا در کلیک روی '{point_name}': {str(e)}")
            self.activity_log.append(
                {
                    "action": "click",
                    "target": point_name,
                    "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "success": False,
                    "error": str(e),
                }
            )
            return False

    def navigate_to(self, url):
        """رفتن به آدرس مشخص"""
        try:
            self.driver.get(url)
            self.human_delay(3, 6)  # صبر برای لود شدن
            print(f"✓ رفتن به: {url}")
            return True
        except Exception as e:
            print(f"خطا در رفتن به {url}: {str(e)}")
            return False

    def add_allowed_point(self, name, selector):
        """اضافه کردن نقطه جدید به لیست مجاز"""
        self.allowed_click_points[name] = selector
        print(f"✓ نقطه '{name}' به لیست مجاز اضافه شد")

    def remove_allowed_point(self, name):
        """حذف نقطه از لیست مجاز"""
        if name in self.allowed_click_points:
            del self.allowed_click_points[name]
            print(f"✓ نقطه '{name}' از لیست مجاز حذف شد")

    def show_allowed_points(self):
        """نمایش لیست نقاط مجاز"""
        print("\n📋 نقاط مجاز برای کلیک:")
        for name, selector in self.allowed_click_points.items():
            print(f"  • {name}: {selector}")

    def show_activity_log(self):
        """نمایش لاگ فعالیت‌ها"""
        print("\n📊 لاگ فعالیت‌ها:")
        for log in self.activity_log[-10:]:  # آخرین 10 فعالیت
            status = "✓" if log["success"] else "✗"
            print(f"  {status} {log['time']} - {log['action']} on {log['target']}")

    def wait_for_element(self, selector, timeout=10):
        """صبر کردن تا المان ظاهر شود"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return element
        except:
            return None

    def close(self):
        """بستن مرورگر"""
        self.driver.quit()
        print("✓ مرورگر بسته شد")


# مثال تست روی ویکی‌پدیا
if __name__ == "__main__":
    # ایجاد ربات
    bot = SafeClickBot(headless=False)

    try:
        print("🚀 شروع تست روی ویکی‌پدیا...")

        # رفتن به صفحه اصلی ویکی‌پدیا فارسی
        bot.navigate_to("https://fa.wikipedia.org")

        # اضافه کردن نقاط کلیک مخصوص ویکی‌پدیا
        bot.add_allowed_point("search_box", "#searchInput")
        bot.add_allowed_point("search_button", "#searchButton")
        bot.add_allowed_point("random_article", "#n-randompage a")
        bot.add_allowed_point("main_page", "#n-mainpage-description a")
        bot.add_allowed_point("help_page", "#n-help a")
        bot.add_allowed_point("first_link", "#mw-content-text p a:first-of-type")

        # نمایش نقاط مجاز
        bot.show_allowed_points()

        print("\n🔍 مرحله 1: کلیک روی جعبه جستجو...")
        bot.safe_click("search_box")

        print("\n🎲 مرحله 2: رفتن به مقاله تصادفی...")
        bot.safe_click("random_article")
        bot.human_delay(3, 5)

        print("\n🔗 مرحله 3: کلیک روی اولین لینک (اگر وجود داشته باشه)...")
        if bot.safe_click("first_link"):
            bot.human_delay(2, 4)

        print("\n🏠 مرحله 4: بازگشت به صفحه اصلی...")
        bot.safe_click("main_page")
        bot.human_delay(2, 3)

        print("\n❓ مرحله 5: رفتن به صفحه راهنما...")
        bot.safe_click("help_page")

        # نمایش لاگ فعالیت‌ها
        print("\n" + "=" * 50)
        bot.show_activity_log()
        print("=" * 50)

        print("\n✅ تست با موفقیت تمام شد!")

    except KeyboardInterrupt:
        print("\n⚠️  برنامه توسط کاربر متوقف شد")

    except Exception as e:
        print(f"\n❌ خطای غیرمنتظره: {str(e)}")

    finally:
        # بستن مرورگر
        print("\n⏸️  برای بستن مرورگر Enter بزنید...")
        input()
        bot.close()


# تست سریع با سایت گوگل
def test_google():
    print("\n🌐 تست سریع با گوگل...")
    bot = SafeClickBot(headless=False)

    try:
        bot.navigate_to("https://www.google.com")

        # نقاط کلیک گوگل
        bot.add_allowed_point("search_box", "input[name='q']")
        bot.add_allowed_point("search_btn", "input[name='btnK']")
        bot.add_allowed_point("feeling_lucky", "input[name='btnI']")
        bot.add_allowed_point("images_tab", "a[href*='tbm=isch']")

        print("کلیک روی جعبه جستجو...")
        bot.safe_click("search_box")

        bot.show_activity_log()

    finally:
        input("Enter برای بستن...")
        bot.close()


# برای اجرای تست گوگل، خط زیر رو uncomment کنید:
# test_google()
