import uuid
import html
import os
import calendar
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client
from datetime import date, timedelta

# ---------------------------------------------------------
# PAGE CONFIG + DARK PRO THEME
# ---------------------------------------------------------
st.set_page_config(
    page_title="BizToolkit",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
:root {
    --bg: #0B1120;
    --panel: #111B2E;
    --panel-2: #162238;
    --border: #263650;
    --text: #E7EEF9;
    --muted: #91A2BC;
    --blue: #4F8CFF;
    --blue-hover: #3977EB;
    --green: #22C58B;
}
.stApp {
    background: var(--bg);
    color: var(--text);
}
[data-testid="stHeader"] {
    background: rgba(11, 17, 32, 0.96);
}
.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3, h4, p, label, .stMarkdown {
    color: var(--text);
}
h1 {
    font-size: 2rem !important;
    font-weight: 750 !important;
    letter-spacing: -0.6px;
}
h2, h3 {
    font-weight: 700 !important;
}
[data-testid="stCaptionContainer"], .stCaption {
    color: var(--muted) !important;
}
[data-testid="stSidebar"] {
    background: #080E1B;
    border-right: 1px solid #1D2A40;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.2rem;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #A9B8CE;
}
.brand-box {
    padding: 8px 8px 22px 8px;
    margin-bottom: 16px;
    border-bottom: 1px solid #263650;
}
.brand-name {
    color: #F8FAFF;
    font-size: 27px;
    font-weight: 850;
    letter-spacing: -1.1px;
    line-height: 1.15;
}
.brand-name span {
    color: #5B96FF;
}
.brand-caption {
    color: #8193AE;
    font-size: 10px;
    letter-spacing: 2px;
    font-weight: 700;
    margin-top: 7px;
}
[data-testid="stRadio"] > div {
    gap: 6px;
}
[data-testid="stRadio"] label {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 10px;
    padding: 9px 12px;
    transition: all .18s ease;
}
[data-testid="stRadio"] label:hover {
    background: #14223A;
    border-color: #263D60;
}
[data-testid="stRadio"] label p {
    color: #B9C7DB !important;
    font-weight: 550;
}
[data-testid="stRadio"] label:has(input:checked) {
    background: #172D4D;
    border: 1px solid #2E5D9D;
}
[data-testid="stRadio"] label:has(input:checked) p {
    color: #FFFFFF !important;
    font-weight: 700;
}
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #142139, #101A2C);
    border: 1px solid #263650;
    border-radius: 15px;
    padding: 19px 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,.13);
}
[data-testid="stMetricLabel"] {
    color: #9FB0C9 !important;
    font-weight: 600;
}
[data-testid="stMetricValue"] {
    color: #F4F7FC !important;
    font-weight: 750;
}
[data-testid="stMetricDelta"] {
    color: #67DDB1 !important;
}
.stButton > button, .stFormSubmitButton > button,
.stDownloadButton > button {
    background: #3478F6;
    color: white !important;
    border: 1px solid #4385FF;
    border-radius: 10px;
    min-height: 42px;
    font-weight: 700;
    transition: all .18s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover,
.stDownloadButton > button:hover {
    background: #2565D8;
    border-color: #6BA0FF;
    color: white !important;
}
.stTextInput input, .stNumberInput input, .stTextArea textarea {
    background: #111D31 !important;
    color: #EDF3FC !important;
    border: 1px solid #30435F !important;
    border-radius: 9px !important;
}
[data-baseweb="select"] > div {
    background: #111D31 !important;
    border-color: #30435F !important;
    border-radius: 9px !important;
    color: #EDF3FC !important;
}
[data-testid="stDateInput"] input {
    background: #111D31 !important;
    color: #EDF3FC !important;
    border-color: #30435F !important;
}
[data-testid="stFileUploader"] {
    background: #111D31;
    border: 1px dashed #3A5275;
    border-radius: 12px;
    padding: 10px;
}
[data-testid="stTabs"] button {
    color: #AFC0D8 !important;
    font-weight: 650;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #76A8FF !important;
}
[data-testid="stDataFrame"], [data-testid="stTable"] {
    border: 1px solid #263650;
    border-radius: 12px;
    overflow: hidden;
}
[data-testid="stExpander"] {
    background: #111B2E;
    border: 1px solid #263650;
    border-radius: 12px;
}
hr {
    border-color: #263650 !important;
}
[data-testid="stAlert"] {
    border-radius: 11px;
}
small, .muted {
    color: #91A2BC;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# LANGUAGE SYSTEM
# ---------------------------------------------------------

TRANSLATIONS = {
    
    "Dashboard": "მთავარი",
    "Products": "პროდუქტები",
    "Sales": "გაყიდვები",
    "Expenses": "ხარჯები",
    "Invoices": "ინვოისები",
    "Analytics": "ანალიტიკა",
    "Business Profile": "ბიზნესის პროფილი",
    "Settings": "პარამეტრები",
    "WORKSPACE": "სამუშაო სივრცე",
    "Revenue": "შემოსავალი",
    "Net profit": "წმინდა მოგება",
    "Products": "პროდუქტები",
    "Units sold": "გაყიდული ერთეულები",
    "Product costs": "პროდუქციის თვითღირებულება",
    "Other expenses": "სხვა ხარჯები",
    "Gross profit": "მთლიანი მოგება",
    "Add product": "პროდუქტის დამატება",
    "Manage products": "პროდუქტების მართვა",
    "Product name": "პროდუქტის სახელი",
    "Selling price (₾)": "გასაყიდი ფასი (₾)",
    "Product cost (₾)": "თვითღირებულება (₾)",
    "Quantity": "რაოდენობა",
    "Save changes": "ცვლილებების შენახვა",
    "Delete": "წაშლა",
    "Record a sale": "გაყიდვის დაფიქსირება",
    "Complete sale": "გაყიდვის დასრულება",
    "Sales history": "გაყიდვების ისტორია",
    "Add expense": "ხარჯის დამატება",
    "Expense history": "ხარჯების ისტორია",
    "Expense description": "ხარჯის აღწერა",
    "Amount (₾)": "თანხა (₾)",
    "Save expense": "ხარჯის შენახვა",
    
    "Daily": "დღიური",
    "Monthly": "თვიური",
    "Yearly": "წლიური",
    "Custom date": "თარიღის არჩევა",
    "Login": "შესვლა",
    "Create account": "ანგარიშის შექმნა",
    "Email": "ელფოსტა",
    "Password": "პაროლი",
    "Logout": "გასვლა",
    "Manage your inventory and product pricing": "მართე მარაგები და პროდუქციის ფასები",
    "＋ Add product": "＋ პროდუქტის დამატება",
    "Manage products": "პროდუქტების მართვა",
    "Enter a product name.": "შეიყვანე პროდუქტის სახელი.",
    "Product added.": "პროდუქტი დაემატა.",
    "Could not add product:": "პროდუქტის დამატება ვერ მოხერხდა:",
    "Choose product": "აირჩიე პროდუქტი",
    "Product name cannot be empty.": "პროდუქტის სახელი ცარიელი არ უნდა იყოს.",
    "Product updated.": "პროდუქტი განახლდა.",
    "Update failed:": "განახლება ვერ მოხერხდა:",
    "Delete selected product": "არჩეული პროდუქტის წაშლა",
    "Product deleted.": "პროდუქტი წაიშალა.",
    "Delete failed:": "წაშლა ვერ მოხერხდა:",
    "No products added yet.": "პროდუქტები ჯერ არ დაგიმატებია.",
    "Inventory": "მარაგები",
    "Your inventory is empty.": "შენი მარაგები ცარიელია.",
    "Record sales and review your sales history": "დააფიქსირე გაყიდვები და ნახე გაყიდვების ისტორია",
    "Record a sale": "გაყიდვის დაფიქსირება",
    "Available stock": "ხელმისაწვდომი მარაგი",
    "Quantity sold": "გაყიდული რაოდენობა",
    "Sale total": "გაყიდვის ჯამი",
    "Sale recorded.": "გაყიდვა დაფიქსირდა.",
    "Could not record sale:": "გაყიდვის დაფიქსირება ვერ მოხერხდა:",
    "Add products with available stock first.": "ჯერ დაამატე პროდუქტები, რომლებსაც მარაგი აქვთ.",
    "Search product": "პროდუქტის ძებნა",
    "Filter by date": "თარიღით გაფილტვრა",
    "sales found": "გაყიდვა მოიძებნა",
    "No sales found for this filter.": "ამ ფილტრით გაყიდვები ვერ მოიძებნა.",
    "No sales recorded yet.": "გაყიდვები ჯერ არ დაფიქსირებულა.",
    "Product": "პროდუქტი",
    "Total": "ჯამი",
    "Profit": "მოგება",
    "Date": "თარიღი",
    "Track and manage your business spending": "აკონტროლე და მართე ბიზნესის ხარჯები",
    "＋ Add expense": "＋ ხარჯის დამატება",
    "Expense history": "ხარჯების ისტორია",
    "Expense description": "ხარჯის აღწერა",
    "Category": "კატეგორია",
    "Save expense": "ხარჯის შენახვა",
    "Enter an expense description.": "შეიყვანე ხარჯის აღწერა.",
    "Amount must be greater than zero.": "თანხა ნულზე მეტი უნდა იყოს.",
    "Expense saved.": "ხარჯი შენახულია.",
    "Could not save expense:": "ხარჯის შენახვა ვერ მოხერხდა:",
    "Total expenses": "საერთო ხარჯები",
    "Delete failed:": "წაშლა ვერ მოხერხდა:",
    "Rent": "ქირა",
    "Electricity": "ელექტროენერგია",
    "Transport": "ტრანსპორტი",
    "Supplies": "მასალები",
    "Marketing": "მარკეტინგი",
    "Salary": "ხელფასი",
    "Maintenance": "მომსახურება",
    "Other": "სხვა",
    "Create, download and manage customer invoices": "შექმენი, ჩამოტვირთე და მართე კლიენტების ინვოისები",
    "Create new invoice": "ახალი ინვოისის შექმნა",
    "Customer name": "კლიენტის სახელი",
    "Invoice total": "ინვოისის ჯამი",
    "Create invoice": "ინვოისის შექმნა",
    "Enter customer name.": "შეიყვანე კლიენტის სახელი.",
    "Not enough stock.": "მარაგი საკმარისი არ არის.",
    "Invoice created.": "ინვოისი შეიქმნა.",
    "Could not create invoice:": "ინვოისის შექმნა ვერ მოხერხდა:",
    "Add products before creating an invoice.": "ინვოისის შესაქმნელად ჯერ დაამატე პროდუქტები.",
    "Invoice history": "ინვოისების ისტორია",
    "Customer": "კლიენტი",
    "Invoice": "ინვოისი",
    "Invoice number": "ინვოისის ნომერი",
    "Price": "ფასი",
    "Print / Save as PDF": "ბეჭდვა / PDF-ად შენახვა",
    "Download invoice": "ინვოისის ჩამოტვირთვა",
    "Delete invoice": "ინვოისის წაშლა",
    "No invoices created yet.": "ინვოისები ჯერ არ შექმნილა.",
    "Business profile": "ბიზნესის პროფილი",
    "Manage your business identity and contact details": "მართე ბიზნესის ინფორმაცია და საკონტაქტო დეტალები",
    "Business information": "ბიზნესის ინფორმაცია",
    "Upload business logo": "ბიზნესის ლოგოს ატვირთვა",
    "New logo preview": "ახალი ლოგოს წინასწარი ნახვა",
    "Current business logo": "მიმდინარე ბიზნესის ლოგო",
    "Business name": "ბიზნესის სახელი",
    "Phone number (9 digits)": "ტელეფონის ნომერი (9 ციფრი)",
    "Business address": "ბიზნესის მისამართი",
    "Business description": "ბიზნესის აღწერა",
    "Save profile": "პროფილის შენახვა",
    "Business name is required.": "ბიზნესის სახელი აუცილებელია.",
    "Phone number must contain exactly 9 digits.": "ტელეფონის ნომერი ზუსტად 9 ციფრისგან უნდა შედგებოდეს.",
    "Business address is required.": "ბიზნესის მისამართი აუცილებელია.",
    "Business description is required.": "ბიზნესის აღწერა აუცილებელია.",
    "Please upload a business logo.": "გთხოვ, ატვირთე ბიზნესის ლოგო.",
    "Logo upload failed:": "ლოგოს ატვირთვა ვერ მოხერხდა:",
    "Business profile saved.": "ბიზნესის პროფილი შენახულია.",
    "Could not save profile:": "პროფილის შენახვა ვერ მოხერხდა:",
    "Profile preview": "პროფილის წინასწარი ნახვა",
    "Phone": "ტელეფონი",
    "Address": "მისამართი",
    "Not added": "არ არის დამატებული",
    "No description": "აღწერა არ არის",
    "Manage your account": "მართე შენი ანგარიში",
    "Account": "ანგარიში",
    "Logged in as": "შესული ხარ როგორც",
    "Your data is stored in your own authenticated workspace.": "შენი მონაცემები ინახება შენს პირად დაცულ სივრცეში.",
    "Logout": "გასვლა",
    "Analytics": "ანალიტიკა",
    "Understand your business performance": "გაიგე შენი ბიზნესის შედეგები",
    "Analytics period": "ანალიტიკის პერიოდი",
    "Choose a day": "აირჩიე დღე",
    "Month": "თვე",
    "Year": "წელი",
    "Choose year": "აირჩიე წელი",
    "Choose date range": "აირჩიე თარიღების შუალედი",
    "Results": "შედეგები",
    "Monthly revenue": "თვიური შემოსავალი",
    "Revenue by day": "შემოსავალი დღეების მიხედვით",
    "Best-selling products": "ყველაზე გაყიდვადი პროდუქტები",
    "No sales found for this period.": "ამ პერიოდში გაყიდვები არ მოიძებნა.",
    "Expenses by category": "ხარჯები კატეგორიების მიხედვით",
    "No expenses found for this period.": "ამ პერიოდში ხარჯები არ მოიძებნა.",
    "Month-to-month comparison": "თვეების შედარება",
    "Previous month": "წინა თვე",
    "Selected month": "არჩეული თვე",
    "Expenses": "ხარჯები",
    "Revenue difference": "შემოსავლის სხვაობა",
    "Net profit difference": "წმინდა მოგების სხვაობა",
    "Export reports": "ანგარიშების ექსპორტი",
    "Download sales report": "გაყიდვების ანგარიშის ჩამოტვირთვა",
    "Download expenses report": "ხარჯების ანგარიშის ჩამოტვირთვა",

    }


def t(text):
    if st.session_state.get("language", "English") == "ქართული":
        return TRANSLATIONS.get(text, text)
    return text

# ---------------------------------------------------------
# CONNECTION
# ---------------------------------------------------------
load_dotenv()

SUPABASE_URL = st.secrets.get(
    "SUPABASE_URL",
    os.getenv("SUPABASE_URL")
)

SUPABASE_KEY = st.secrets.get(
    "SUPABASE_KEY",
    os.getenv("SUPABASE_KEY")
)

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Supabase credentials are missing. Check your .env file.")
    st.stop()

if "supabase" not in st.session_state:
    try:
        st.session_state.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        st.error(f"Registration failed: {e}")

supabase = st.session_state.supabase

# ---------------------------------------------------------
# AUTHENTICATION
# ---------------------------------------------------------
if "user_id" not in st.session_state:
    st.markdown("""
    <div style="max-width:760px;margin:5vh auto 25px auto;text-align:center;">
      <div style="font-size:15px;color:#7FAEFF;font-weight:800;letter-spacing:3px;">
        BUSINESS MANAGEMENT
      </div>
      <div style="font-size:48px;font-weight:900;letter-spacing:-2px;color:#F4F7FC;">
        Biz<span style="color:#5B96FF;">Toolkit</span>
      </div>
      <div style="color:#91A2BC;font-size:15px;">
        Your business. Your numbers. Your control.
      </div>
    </div>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1, 1.25, 1])
    with center:
        login_tab, register_tab = st.tabs(["Login", "Create account"])

        with login_tab:
            st.subheader("Welcome back")
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                login = st.form_submit_button("Login", use_container_width=True)
                if login:
                    try:
                        response = supabase.auth.sign_in_with_password({
                            "email": email.strip(),
                            "password": password
                        })
                        if response.session:
                            st.session_state.user_id = response.user.id
                            st.session_state.user_email = response.user.email
                            st.rerun()
                        else:
                            st.error("Login session was not created.")
                    except Exception:
                        st.error("Login failed. Check your email and password.")

        with register_tab:
            st.subheader("Create your account")
            with st.form("register_form"):
                new_email = st.text_input("Email address")
                new_password = st.text_input("Password", type="password")
                confirm = st.text_input("Confirm password", type="password")
                register = st.form_submit_button("Create account", use_container_width=True)

                if register:
                    if not new_email.strip() or not new_password:
                        st.error("Fill in all fields.")
                    elif new_password != confirm:
                        st.error("Passwords do not match.")
                    elif len(new_password) < 6:
                        st.error("Password must contain at least 6 characters.")
                    else:
                        try:
                            response = supabase.auth.sign_up({
                                "email": new_email.strip(),
                                "password": new_password
                            })
                            if response.session:
                                st.session_state.user_id = response.user.id
                                st.session_state.user_email = response.user.email
                                st.rerun()
                            else:
                                st.success("Account created! Confirm your email, then log in.")
                        except Exception:
                            st.error("Registration failed. Check your details.")
    st.stop()

user_id = st.session_state.user_id
user_email = st.session_state.user_email

# ---------------------------------------------------------
# DATABASE HELPERS
# ---------------------------------------------------------
def fetch_table(table, order_column="created_at"):
    return (
        supabase.table(table)
        .select("*")
        .order(order_column, desc=True)
        .execute()
        .data or []
    )

def get_products():
    return fetch_table("products")

def get_sales():
    return fetch_table("sales")

def get_expenses():
    return fetch_table("expenses")

def get_invoices():
    return fetch_table("invoices")

def get_business_profile():
    result = (
        supabase.table("business_profiles")
        .select("*")
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )
    return result.data[0] if result.data else None

# ---------------------------------------------------------
# DATA PROCESSING
# ---------------------------------------------------------
def sales_dataframe(items):
    if not items:
        return pd.DataFrame()
    frame = pd.DataFrame(items)
    frame["created_at"] = pd.to_datetime(
        frame["created_at"], utc=True
    ).dt.tz_convert("Asia/Tbilisi")
    frame["date"] = frame["created_at"].dt.date
    for col in ["total", "unit_cost", "quantity"]:
        frame[col] = pd.to_numeric(frame[col])
    frame["profit"] = frame["total"] - frame["unit_cost"] * frame["quantity"]
    return frame

def expenses_dataframe(items):
    if not items:
        return pd.DataFrame()
    frame = pd.DataFrame(items)
    frame["created_at"] = pd.to_datetime(
        frame["created_at"], utc=True
    ).dt.tz_convert("Asia/Tbilisi")
    frame["date"] = frame["created_at"].dt.date
    frame["amount"] = pd.to_numeric(frame["amount"])
    return frame

def calculate_metrics(sales_data, expense_data):
    revenue = sales_data["total"].sum() if not sales_data.empty else 0
    product_costs = (
        (sales_data["unit_cost"] * sales_data["quantity"]).sum()
        if not sales_data.empty else 0
    )
    other_expenses = expense_data["amount"].sum() if not expense_data.empty else 0
    gross_profit = revenue - product_costs
    net_profit = gross_profit - other_expenses
    units = sales_data["quantity"].sum() if not sales_data.empty else 0
    return {
        "revenue": float(revenue),
        "product_costs": float(product_costs),
        "other_expenses": float(other_expenses),
        "total_expenses": float(product_costs + other_expenses),
        "gross_profit": float(gross_profit),
        "net_profit": float(net_profit),
        "units": int(units)
    }

try:
    products = get_products()
    sales = get_sales()
    expenses = get_expenses()
    df = sales_dataframe(sales)
    expense_df = expenses_dataframe(expenses)
except Exception as e:
    st.error(f"Could not load business data: {e}")
    st.stop()

# ---------------------------------------------------------
# SIDEBAR / BRAND
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="brand-box">
      <div class="brand-name">Biz<span>Toolkit</span></div>
      <div class="brand-caption">BUSINESS MANAGEMENT</div>
    </div>
    """, unsafe_allow_html=True)
    
    language = st.selectbox(
        "Language / ენა",
        ["English", "ქართული"],
        key="language"
    )
    st.markdown(
        f"<div style='font-size:12px;color:#8FA2BE;margin:0 0 15px 4px;'>"
        f"SIGNED IN AS<br><b style='color:#E7EEF9;'>{html.escape(user_email)}</b></div>",
        unsafe_allow_html=True
    )
    pages = [
        "Dashboard",
        "Products",
        "Sales",
        "Expenses",
        "Invoices",
        "Analytics",
        "Business Profile",
        "Settings"
    ]

    selected_page = st.radio(
        t("WORKSPACE"),
        pages,
        format_func=t,
        label_visibility="visible"
    )

    page = selected_page

# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------
if page == "Dashboard":
    st.title(t("Dashboard"))
    st.caption(t("Your business overview at a glance"))

    low_stock = [p for p in products if int(p["quantity"]) <= 5]

    if low_stock:
        with st.container(border=True):
            st.subheader(t("Stock alerts"))
            for product in low_stock:
                qty = int(product["quantity"])
                if qty == 0:
                    st.error(f"{product['name']} — {t('Out of stock')}")
                else:
                    st.warning(f"{product['name']} — {t('Only')} {qty} {t('left')}")
    else:
        st.success(t("All products have sufficient stock."))

    metrics = calculate_metrics(df, expense_df)

    a, b, c, d = st.columns(4)
    a.metric(t("Revenue"), f"₾{metrics['revenue']:,.2f}")
    b.metric(t("Net profit"), f"₾{metrics['net_profit']:,.2f}")
    c.metric(t("Products"), len(products))
    d.metric(t("Units sold"), metrics["units"])

    a, b, c = st.columns(3)
    a.metric(t("Product costs"), f"₾{metrics['product_costs']:,.2f}")
    b.metric(t("Other expenses"), f"₾{metrics['other_expenses']:,.2f}")
    c.metric(t("Gross profit"), f"₾{metrics['gross_profit']:,.2f}")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader(t("Recent sales"))
        if not df.empty:
            for _, sale in df.head(5).iterrows():
                with st.container(border=True):
                    st.write(f"**{sale['product_name']}**")
                    st.write(
                        f"{int(sale['quantity'])} {t('pcs')}  ·  ₾{sale['total']:.2f}"
                    )
                    st.caption(sale["created_at"].strftime("%d.%m.%Y %H:%M"))
        else:
            st.info(t("No sales yet."))

    with right:
        st.subheader(t("Recent expenses"))
        if not expense_df.empty:
            for _, expense in expense_df.head(5).iterrows():
                with st.container(border=True):
                    st.write(f"**{expense['title']}**")
                    st.write(f"₾{expense['amount']:.2f}")
                    st.caption(
                        f"{t(expense['category'])}  ·  "
                        f"{expense['created_at'].strftime('%d.%m.%Y %H:%M')}"
                    )
        else:
            st.info(t("No expenses yet."))

# ---------------------------------------------------------
# PRODUCTS
# ---------------------------------------------------------
elif page == "Products":
    st.title(t("Products"))
    st.caption(t("Manage your inventory and product pricing"))

    add_tab, manage_tab = st.tabs([
        t("＋ Add product"),
        t("Manage products")
    ])

    with add_tab:
        with st.form("add_product"):
            name = st.text_input(t("Product name"))
            a, b, c = st.columns(3)

            price = a.number_input(t("Selling price (₾)"), min_value=0.0)
            cost = b.number_input(t("Product cost (₾)"), min_value=0.0)
            quantity = c.number_input(t("Quantity"), min_value=0, step=1)

            submit = st.form_submit_button(
                t("Add product"), use_container_width=True
            )

            if submit:
                if not name.strip():
                    st.error(t("Enter a product name."))
                else:
                    try:
                        supabase.table("products").insert({
                            "user_id": user_id,
                            "name": name.strip(),
                            "price": price,
                            "cost": cost,
                            "quantity": quantity
                        }).execute()

                        st.success(t("Product added."))
                        st.rerun()

                    except Exception as e:
                        st.error(f"{t('Could not add product:')} {e}")

    with manage_tab:
        if products:
            selected_index = st.selectbox(
                t("Choose product"),
                range(len(products)),
                format_func=lambda i: products[i]["name"]
            )

            product = products[selected_index]

            with st.form("edit_product"):
                new_name = st.text_input(
                    t("Product name"), value=product["name"]
                )

                a, b, c = st.columns(3)

                new_price = a.number_input(
                    t("Selling price (₾)"),
                    min_value=0.0,
                    value=float(product["price"])
                )

                new_cost = b.number_input(
                    t("Product cost (₾)"),
                    min_value=0.0,
                    value=float(product["cost"])
                )

                new_quantity = c.number_input(
                    t("Quantity"),
                    min_value=0,
                    value=int(product["quantity"])
                )

                update = st.form_submit_button(
                    t("Save changes"), use_container_width=True
                )

                if update:
                    if not new_name.strip():
                        st.error(t("Product name cannot be empty."))
                    else:
                        try:
                            supabase.table("products").update({
                                "name": new_name.strip(),
                                "price": new_price,
                                "cost": new_cost,
                                "quantity": new_quantity
                            }).eq("id", product["id"]).execute()

                            st.success(t("Product updated."))
                            st.rerun()

                        except Exception as e:
                            st.error(f"{t('Update failed:')} {e}")

            if st.button(t("Delete selected product"), type="secondary"):
                try:
                    supabase.table("products").delete().eq(
                        "id", product["id"]
                    ).execute()

                    st.success(t("Product deleted."))
                    st.rerun()

                except Exception as e:
                    st.error(f"{t('Delete failed:')} {e}")

        else:
            st.info(t("No products added yet."))

    st.divider()
    st.subheader(t("Inventory"))

    if products:
        inventory_df = pd.DataFrame(products)[
            ["name", "price", "cost", "quantity"]
        ].rename(columns={
            "name": t("Product name"),
            "price": t("Selling price (₾)"),
            "cost": t("Product cost (₾)"),
            "quantity": t("Quantity")
        })

        st.dataframe(inventory_df, use_container_width=True, hide_index=True)

    else:
        st.info(t("Your inventory is empty."))

# ---------------------------------------------------------
# SALES
# ---------------------------------------------------------
elif page == "Sales":
    st.title(t("Sales"))
    st.caption(t("Record sales and review your sales history"))

    available = [p for p in products if int(p["quantity"]) > 0]

    if available:
        with st.container(border=True):
            st.subheader(t("Record a sale"))

            selected = st.selectbox(
                t("Choose product"), available,
                format_func=lambda p: p["name"]
            )

            st.caption(f"{t('Available stock')}: {selected['quantity']}")

            quantity = st.number_input(
                t("Quantity sold"), min_value=1,
                max_value=int(selected["quantity"]), step=1
            )

            total = float(selected["price"]) * quantity
            st.metric(t("Sale total"), f"₾{total:.2f}")

            if st.button(t("Complete sale"), use_container_width=True):
                try:
                    supabase.rpc("record_sale", {
                        "p_product_id": selected["id"],
                        "p_quantity": int(quantity)
                    }).execute()

                    st.success(t("Sale recorded."))
                    st.rerun()

                except Exception as e:
                    st.error(f"{t('Could not record sale:')} {e}")

    else:
        st.info(t("Add products with available stock first."))

    st.divider()
    st.subheader(t("Sales history"))

    if not df.empty:
        search = st.text_input(t("Search product"))

        filtered = df[df["product_name"].str.contains(
            search, case=False, na=False
        )]

        date_range = st.date_input(
            t("Filter by date"),
            value=(date.today() - timedelta(days=30), date.today()),
            key="sales_date_filter"
        )

        if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
            start_date, end_date = date_range

            filtered = filtered[
                (filtered["date"] >= start_date) &
                (filtered["date"] <= end_date)
            ]

        st.caption(f"{len(filtered)} {t('sales found')}")

        if not filtered.empty:
            sales_display = filtered[
                ["product_name", "quantity", "total", "profit", "created_at"]
            ].rename(columns={
                "product_name": t("Product"),
                "quantity": t("Quantity"),
                "total": t("Total"),
                "profit": t("Profit"),
                "created_at": t("Date")
            })

            st.dataframe(
                sales_display,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info(t("No sales found for this filter."))

    else:
        st.info(t("No sales recorded yet."))

# ---------------------------------------------------------
# EXPENSES
# ---------------------------------------------------------
elif page == "Expenses":
    st.title(t("Expenses"))
    st.caption(t("Track and manage your business spending"))

    categories = [
        "Rent", "Electricity", "Transport", "Supplies",
        "Marketing", "Salary", "Maintenance", "Other"
    ]

    add_tab, history_tab = st.tabs([
        t("＋ Add expense"),
        t("Expense history")
    ])

    with add_tab:
        with st.form("add_expense"):
            title = st.text_input(t("Expense description"))

            a, b = st.columns(2)

            category = a.selectbox(
                t("Category"),
                categories,
                format_func=t
            )

            amount = b.number_input(
                t("Amount (₾)"), min_value=0.0, step=1.0
            )

            submit_expense = st.form_submit_button(
                t("Save expense"), use_container_width=True
            )

            if submit_expense:
                if not title.strip():
                    st.error(t("Enter an expense description."))
                elif amount <= 0:
                    st.error(t("Amount must be greater than zero."))
                else:
                    try:
                        supabase.table("expenses").insert({
                            "user_id": user_id,
                            "title": title.strip(),
                            "category": category,
                            "amount": amount
                        }).execute()

                        st.success(t("Expense saved."))
                        st.rerun()

                    except Exception as e:
                        st.error(f"{t('Could not save expense:')} {e}")

    with history_tab:
        if expenses:
            st.metric(
                t("Total expenses"),
                f"₾{expense_df['amount'].sum():,.2f}"
            )

            for expense in expenses:
                with st.container(border=True):
                    a, b = st.columns([4, 1])

                    a.write(f"**{expense['title']}**")

                    a.write(
                        f"₾{float(expense['amount']):.2f}  ·  "
                        f"{t(expense['category'])}"
                    )

                    a.caption(
                        pd.to_datetime(
                            expense["created_at"]
                        ).strftime("%d.%m.%Y")
                    )

                    if b.button(
                        t("Delete"),
                        key=f"delete_expense_{expense['id']}"
                    ):
                        try:
                            supabase.table("expenses").delete().eq(
                                "id", expense["id"]
                            ).execute()

                            st.rerun()

                        except Exception as e:
                            st.error(f"{t('Delete failed:')} {e}")

        else:
            st.info(t("No expenses recorded yet."))

# ---------------------------------------------------------
# INVOICES
# ---------------------------------------------------------

elif page == "Invoices":
    st.title(t("Invoices"))
    st.caption(t("Create, download and manage customer invoices"))

    invoices = get_invoices()
    st.subheader(t("Create new invoice"))

    if products:
        with st.form("create_invoice"):
            customer_name = st.text_input(t("Customer name"))

            selected_product = st.selectbox(
                t("Choose product"), products,
                format_func=lambda p: p["name"]
            )

            invoice_quantity = st.number_input(
                t("Quantity"), min_value=1,
                max_value=max(1, int(selected_product["quantity"])),
                step=1
            )

            unit_price = float(selected_product["price"])
            invoice_total = unit_price * invoice_quantity

            st.metric(t("Invoice total"), f"₾{invoice_total:.2f}")

            create = st.form_submit_button(
                t("Create invoice"), use_container_width=True
            )

            if create:
                if not customer_name.strip():
                    st.error(t("Enter customer name."))
                elif int(selected_product["quantity"]) < invoice_quantity:
                    st.error(t("Not enough stock."))
                else:
                    try:
                        invoice_number = (
                            f"INV-{date.today().strftime('%Y%m%d')}-"
                            f"{len(invoices) + 1:04d}"
                        )

                        invoice_items = [{
                            "product_name": selected_product["name"],
                            "quantity": int(invoice_quantity),
                            "unit_price": unit_price,
                            "total": invoice_total
                        }]

                        supabase.table("invoices").insert({
                            "user_id": user_id,
                            "invoice_number": invoice_number,
                            "customer_name": customer_name.strip(),
                            "items": invoice_items,
                            "total": invoice_total
                        }).execute()

                        st.success(t("Invoice created."))
                        st.rerun()

                    except Exception as e:
                        st.error(f"{t('Could not create invoice:')} {e}")

    else:
        st.info(t("Add products before creating an invoice."))

    st.divider()
    st.subheader(t("Invoice history"))

    if invoices:
        for invoice in invoices:
            with st.expander(
                f"{invoice['invoice_number']}  ·  "
                f"{invoice['customer_name']}  ·  "
                f"₾{float(invoice['total']):.2f}"
            ):
                st.write(
                    f"{t('Customer')}: {invoice['customer_name']}"
                )

                for item in invoice["items"]:
                    st.write(
                        f"{item['product_name']} × {item['quantity']} — "
                        f"₾{float(item['total']):.2f}"
                    )

                st.write(
                    f"**{t('Total')}: ₾{float(invoice['total']):.2f}**"
                )

                invoice_html = f"""
                <html>
                <head>
                <meta charset="UTF-8">
                <title>{t("Invoice")}</title>
                <style>
                body {{font-family:Arial;padding:40px;color:#222;}}
                h1 {{color:#2563EB;}}
                table {{width:100%;border-collapse:collapse;}}
                td,th {{padding:12px;border-bottom:1px solid #ddd;text-align:left;}}
                .total {{text-align:right;font-size:22px;}}
                </style>
                </head>
                <body>
                <h1>BIZTOOLKIT</h1>
                <h2>{t("Invoice")}</h2>
                <p>{t("Invoice number")}: {html.escape(str(invoice['invoice_number']))}</p>
                <p>{t("Customer")}: {html.escape(str(invoice['customer_name']))}</p>

                <table>
                <tr>
                <th>{t("Product")}</th>
                <th>{t("Quantity")}</th>
                <th>{t("Price")}</th>
                <th>{t("Total")}</th>
                </tr>
                """

                for item in invoice["items"]:
                    invoice_html += f"""
                    <tr>
                    <td>{html.escape(str(item['product_name']))}</td>
                    <td>{int(item['quantity'])}</td>
                    <td>₾{float(item['unit_price']):.2f}</td>
                    <td>₾{float(item['total']):.2f}</td>
                    </tr>
                    """

                invoice_html += f"""
                </table>
                <h2 class="total">
                {t("Total")}: ₾{float(invoice['total']):.2f}
                </h2>
                <button onclick="window.print()">
                {t("Print / Save as PDF")}
                </button>
                </body>
                </html>
                """

                st.download_button(
                    t("Download invoice"),
                    data=invoice_html,
                    file_name=f"{invoice['invoice_number']}.html",
                    mime="text/html",
                    key=f"download_{invoice['id']}"
                )

                if st.button(
                    t("Delete invoice"),
                    key=f"delete_{invoice['id']}"
                ):
                    try:
                        supabase.table("invoices").delete().eq(
                            "id", invoice["id"]
                        ).execute()

                        st.rerun()

                    except Exception as e:
                        st.error(f"{t('Delete failed:')} {e}")

    else:
        st.info(t("No invoices created yet."))

# ---------------------------------------------------------
# BUSINESS PROFILE
# ---------------------------------------------------------
elif page == "Business Profile":
    st.title(t("Business profile"))
    st.caption(t("Manage your business identity and contact details"))

    profile = get_business_profile() or {}

    default_name = profile.get("business_name", "")
    default_phone = profile.get("phone", "")
    default_address = profile.get("address", "")
    default_description = profile.get("description", "")
    default_logo = profile.get("logo_url", "")

    st.subheader(t("Business information"))

    uploaded_logo = st.file_uploader(
        t("Upload business logo"),
        type=["png", "jpg", "jpeg", "webp"],
        key="business_logo_upload"
    )

    if uploaded_logo:
        st.image(uploaded_logo, caption=t("New logo preview"), width=170)
    elif default_logo:
        st.image(default_logo, caption=t("Current business logo"), width=170)

    with st.form("business_profile_form"):
        business_name = st.text_input(
            t("Business name"), value=default_name
        )

        phone = st.text_input(
            t("Phone number (9 digits)"),
            value=default_phone,
            max_chars=9
        )

        address = st.text_input(
            t("Business address"), value=default_address
        )

        description = st.text_area(
            t("Business description"), value=default_description
        )

        save = st.form_submit_button(
            t("Save profile"), use_container_width=True
        )

    if save:
        clean_phone = phone.strip().replace(" ", "")

        if not business_name.strip():
            st.error(t("Business name is required."))
        elif not clean_phone.isdigit() or len(clean_phone) != 9:
            st.error(t("Phone number must contain exactly 9 digits."))
        elif not address.strip():
            st.error(t("Business address is required."))
        elif not description.strip():
            st.error(t("Business description is required."))
        elif not uploaded_logo and not default_logo:
            st.error(t("Please upload a business logo."))
        else:
            final_logo_url = default_logo

            try:
                if uploaded_logo:
                    extension = uploaded_logo.name.rsplit(".", 1)[-1].lower()
                    file_path = f"{user_id}/{uuid.uuid4().hex}.{extension}"

                    supabase.storage.from_("business-logos").upload(
                        file_path,
                        uploaded_logo.getvalue(),
                        {
                            "content-type": uploaded_logo.type,
                            "upsert": "true"
                        }
                    )

                    final_logo_url = (
                        supabase.storage.from_("business-logos")
                        .get_public_url(file_path)
                    )

            except Exception as e:
                st.error(f"{t('Logo upload failed:')} {e}")
                st.stop()

            profile_data = {
                "user_id": user_id,
                "business_name": business_name.strip(),
                "phone": clean_phone,
                "address": address.strip(),
                "description": description.strip(),
                "logo_url": final_logo_url
            }

            try:
                if profile:
                    supabase.table("business_profiles").update(
                        profile_data
                    ).eq("user_id", user_id).execute()
                else:
                    supabase.table("business_profiles").insert(
                        profile_data
                    ).execute()

                st.success(t("Business profile saved."))
                st.rerun()

            except Exception as e:
                st.error(f"{t('Could not save profile:')} {e}")

    if profile.get("business_name"):
        st.divider()
        st.subheader(t("Profile preview"))

        a, b = st.columns([1, 3])

        with a:
            if profile.get("logo_url"):
                st.image(profile["logo_url"], width=170)

        with b:
            st.write(f"**{profile['business_name']}**")
            st.write(
                f"{t('Phone')}: {profile.get('phone') or t('Not added')}"
            )
            st.write(
                f"{t('Address')}: {profile.get('address') or t('Not added')}"
            )
            st.write(
                profile.get("description") or t("No description")
            )



elif page == "Analytics":
    st.title(t("Analytics"))
    st.caption(t("Understand your business performance"))

    today = date.today()

    view = st.selectbox(
        t("Analytics period"),
        ["Daily", "Monthly", "Yearly", "Custom date"],
        format_func=t
    )

    filtered_sales = pd.DataFrame()
    filtered_expenses = pd.DataFrame()

    selected_start = None
    selected_end = None

    all_years = {today.year}

    if not df.empty:
        all_years.update(df["date"].apply(lambda d: d.year).tolist())

    if not expense_df.empty:
        all_years.update(
            expense_df["date"].apply(lambda d: d.year).tolist()
        )

    available_years = sorted(all_years)

    if view == "Daily":
        selected_start = st.date_input(
            t("Choose a day"),
            value=today,
            key="analytics_daily"
        )
        selected_end = selected_start

    elif view == "Monthly":
        a, b = st.columns(2)

        selected_month = a.selectbox(
            t("Month"),
            list(range(1, 13)),
            index=today.month - 1,
            format_func=lambda m: (
                [
                    "იანვარი", "თებერვალი", "მარტი", "აპრილი",
                    "მაისი", "ივნისი", "ივლისი", "აგვისტო",
                    "სექტემბერი", "ოქტომბერი", "ნოემბერი", "დეკემბერი"
                ][m - 1]
                if st.session_state.get("language") == "ქართული"
                else calendar.month_name[m]
            )
        )

        selected_year = b.selectbox(
            t("Year"),
            available_years,
            index=available_years.index(today.year)
        )

        selected_start = date(selected_year, selected_month, 1)

        selected_end = date(
            selected_year,
            selected_month,
            calendar.monthrange(selected_year, selected_month)[1]
        )

    elif view == "Yearly":
        selected_year = st.selectbox(
            t("Choose year"),
            available_years,
            index=available_years.index(today.year)
        )

        selected_start = date(selected_year, 1, 1)
        selected_end = date(selected_year, 12, 31)

    else:
        default_start = today - timedelta(days=29)

        if not df.empty:
            default_start = min(default_start, min(df["date"]))

        if not expense_df.empty:
            default_start = min(default_start, min(expense_df["date"]))

        date_range = st.date_input(
            t("Choose date range"),
            value=(default_start, today),
            key="analytics_custom"
        )

        if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
            selected_start, selected_end = date_range

    if selected_start and selected_end:

        if not df.empty:
            filtered_sales = df[
                (df["date"] >= selected_start) &
                (df["date"] <= selected_end)
            ].copy()

        if not expense_df.empty:
            filtered_expenses = expense_df[
                (expense_df["date"] >= selected_start) &
                (expense_df["date"] <= selected_end)
            ].copy()

        metrics = calculate_metrics(filtered_sales, filtered_expenses)

        st.divider()

        st.subheader(
            f"{t('Results')}: "
            f"{selected_start.strftime('%d.%m.%Y')} – "
            f"{selected_end.strftime('%d.%m.%Y')}"
        )

        a, b, c, d = st.columns(4)

        a.metric(t("Revenue"), f"₾{metrics['revenue']:,.2f}")
        b.metric(t("Total expenses"), f"₾{metrics['total_expenses']:,.2f}")
        c.metric(t("Net profit"), f"₾{metrics['net_profit']:,.2f}")
        d.metric(t("Units sold"), metrics["units"])

        a, b, c = st.columns(3)

        a.metric(t("Product costs"), f"₾{metrics['product_costs']:,.2f}")
        b.metric(t("Other expenses"), f"₾{metrics['other_expenses']:,.2f}")
        c.metric(t("Gross profit"), f"₾{metrics['gross_profit']:,.2f}")

        st.divider()

        if not filtered_sales.empty:

            if view == "Yearly":
                st.subheader(t("Monthly revenue"))

                monthly = filtered_sales.groupby(
                    filtered_sales["created_at"].dt.month
                )["total"].sum()

                month_names = (
                    [
                        "იანვარი", "თებერვალი", "მარტი", "აპრილი",
                        "მაისი", "ივნისი", "ივლისი", "აგვისტო",
                        "სექტემბერი", "ოქტომბერი", "ნოემბერი", "დეკემბერი"
                    ]
                    if st.session_state.get("language") == "ქართული"
                    else list(calendar.month_name)[1:]
                )

                monthly.index = [
                    month_names[int(m) - 1]
                    for m in monthly.index
                ]

                st.bar_chart(monthly)

            else:
                st.subheader(t("Revenue by day"))
                st.bar_chart(
                    filtered_sales.groupby("date")["total"].sum()
                )

            st.subheader(t("Best-selling products"))

            best = filtered_sales.groupby(
                "product_name"
            )["quantity"].sum().sort_values(ascending=False)

            st.bar_chart(best)

        else:
            st.info(t("No sales found for this period."))

        if not filtered_expenses.empty:
            st.subheader(t("Expenses by category"))

            expense_chart = filtered_expenses.copy()

            if st.session_state.get("language") == "ქართული":
                expense_chart["category"] = expense_chart["category"].map(t)

            st.bar_chart(
                expense_chart.groupby("category")["amount"]
                .sum()
                .sort_values(ascending=False)
            )

        else:
            st.info(t("No expenses found for this period."))

        if view == "Monthly":

            st.divider()
            st.subheader(t("Month-to-month comparison"))

            previous_month = selected_month - 1
            previous_year = selected_year

            if previous_month == 0:
                previous_month = 12
                previous_year -= 1

            previous_start = date(previous_year, previous_month, 1)

            previous_end = date(
                previous_year,
                previous_month,
                calendar.monthrange(previous_year, previous_month)[1]
            )

            previous_sales = (
                df[
                    (df["date"] >= previous_start) &
                    (df["date"] <= previous_end)
                ]
                if not df.empty else pd.DataFrame()
            )

            previous_expenses = (
                expense_df[
                    (expense_df["date"] >= previous_start) &
                    (expense_df["date"] <= previous_end)
                ]
                if not expense_df.empty else pd.DataFrame()
            )

            previous_metrics = calculate_metrics(
                previous_sales,
                previous_expenses
            )

            comparison = pd.DataFrame({
                t("Previous month"): [
                    previous_metrics["revenue"],
                    previous_metrics["total_expenses"],
                    previous_metrics["net_profit"]
                ],
                t("Selected month"): [
                    metrics["revenue"],
                    metrics["total_expenses"],
                    metrics["net_profit"]
                ]
            }, index=[
                t("Revenue"),
                t("Expenses"),
                t("Net profit")
            ])

            st.bar_chart(comparison)

            a, b = st.columns(2)

            revenue_difference = (
                metrics["revenue"] - previous_metrics["revenue"]
            )

            profit_difference = (
                metrics["net_profit"] - previous_metrics["net_profit"]
            )

            a.metric(
                t("Revenue difference"),
                f"₾{revenue_difference:,.2f}"
            )

            b.metric(
                t("Net profit difference"),
                f"₾{profit_difference:,.2f}"
            )

        st.divider()
        st.subheader(t("Export reports"))

        a, b = st.columns(2)

        with a:
            if not filtered_sales.empty:
                st.download_button(
                    t("Download sales report"),
                    filtered_sales.to_csv(index=False).encode("utf-8-sig"),
                    "biztoolkit_sales_report.csv",
                    "text/csv",
                    use_container_width=True
                )

        with b:
            if not filtered_expenses.empty:
                st.download_button(
                    t("Download expenses report"),
                    filtered_expenses.to_csv(index=False).encode("utf-8-sig"),
                    "biztoolkit_expenses_report.csv",
                    "text/csv",
                    use_container_width=True
                )



# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------
elif page == "Settings":
    st.title(t("Settings"))
    st.caption(t("Manage your account"))

    with st.container(border=True):
        st.subheader(t("Account"))
        st.write(f"{t('Logged in as')}: **{user_email}**")
        st.caption(t("Your data is stored in your own authenticated workspace."))

    st.divider()

    if st.button(t("Logout"), type="secondary"):
        try:
            supabase.auth.sign_out()
        finally:
            st.session_state.pop("user_id", None)
            st.session_state.pop("user_email", None)
            st.rerun()
