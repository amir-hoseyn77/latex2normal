# Convert latex format to normal format (e.g. notepad)
# تبدیل فرمت لاتک به حالت عادی (مثل نوت‌پد) و بالعکس

بعضی اول در ورد متنشان را می‌نویسند و ویرایش می‌کنند و بعد در لاتک می‌نویسند. همانطور که می‌دانید در لاتک برای نوشتن  متون فارسی باید از بسته xepersian استفاده کرد اما اینجوری برای نوشتن کلمات انگلیسی نیازمند تگ `\lr{}` هستیم. برای همین این نرم‌افزار (با اغماض!) سعی کرده جلوی پیدا کردن دستی کلمات انگلیسی متن و گذاشتن آنها در تگ `\lr{}` را بگیرد که حداقل برای من در متون با حجم متوسط هم عذاب‌آور است.
البته سعی شده که چند ویژگی دیگر هم داشته باشد مثلا حفظ فرمت فرمول‌ها در تغییر بین لاتک و معمولی (منظورم word یا notepad است) یا درج خودکار علامات خاص (# $ % & ~ _ ^ \ { }) که در فرمت عادی راحت استفاده می‌کنیم اما باید به لاتک تفهیم کرد.

این نرم‌افزار در ۴ مود فعالیت می‌کند:

1. تبدیل فرمت لاتک به فرمت عادی

2. تبدیل فرمت عادی به لاتک

3. تبدیل اعداد انگلیسی به فارسی

4. تبدیل اعداد فارسی به انگلیسی

## ضعف در GUI
من خیلی رابط گرافیکی پایتون بلد نیستم و برای همین بهتر است مستقیم کپی و پیست کنید و اصلا به آنچه نمایش داده می‌شود اعتماد نکنید (مثل شکل زیر). امیدوارم درگام‌های بعدی این مورد هم درست شود.

![GUI weakness!](/images/lat_GUI.png)

## بررسی آپشن‌های اجرا

یک لیست که یکی از ۴مود بالا را در آن انتخاب می‌کنیم. همچنین ۵ دکمه داریم که آن‌ها را بررسی می‌کنیم. البته بنظرم همان گزینه `All in 1` بهتر است و توصیه می‌شود:
-`Paste`: پیست کردن از کلیپ‌بورد به تکست‌باکس  ورودی
-`Copy`: کپی‌کردن از  تکست‌باکس  خروجی به کلیپ‌بورد
-`Process->Copy`: پردازش (از لیست انتخاب شده) و کپی در کلیپ‌بورد
-`Process->Paste`: ترکیب دو دکمه `Process` و `Paste`. یعنی پردازش می‌کند و سپس آن‌ها را در تکست‌باکس ورودی می‌ریزد. مناسب برای کارهای زنجیره‌ای مثلا اول همه اعداد را انگلیسی کنیم و بعد آن را به فرمت لاتک ببریم.
-`All in 1`: آنچه خوبان همه دارند! از کلیپ بورد می‌خواند و پردازش را انجام می‌دهد و سپس به کلیپ برد برمی‌گرداند.
