# ============================================================
# ANTHOBIZ v1.3.2 - MODERN FINAL FOR APK
# ANTHO-TECH SOLUTIONS - With Logo & Modern UI
# Firmware • Hardware • Electronics • Programming • Coding
# ============================================================

import json
import os
import uuid
from datetime import datetime

from kivy.app import App
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image

APP_VERSION = "1.3.2"
LOGO_FILE = "logo.png"

def get_db_path():
    try:
        from android.storage import app_storage_path
        folder = app_storage_path()
        if not os.path.exists(folder):
            os.makedirs(folder)
        return os.path.join(folder, "anthobiz_data.json")
    except:
        try:
            base = App.get_running_app().user_data_dir
            return os.path.join(base, "anthobiz_data.json")
        except:
            return os.path.join(os.path.dirname(os.path.abspath(__file__)), "anthobiz_data.json")

DATABASE = get_db_path()
STATUSES = ["Pending", "In Progress", "Ready"]
# MODERN DARK NAVY BLUE BACKGROUND
Window.clearcolor = (0.03, 0.08, 0.18, 1)

def empty_database():
    return {"repairs": [], "stock": [], "sales": [], "expenses": []}

def load_database():
    if not os.path.exists(DATABASE):
        return empty_database()
    try:
        with open(DATABASE, "r", encoding="utf-8") as file:
            data = json.load(file)
        for key in ("repairs", "stock", "sales", "expenses"):
            if key not in data:
                data[key] = []
        return data
    except Exception as exc:
        raise RuntimeError(f"Could not read database.\n{exc}")

def save_database(data):
    temp_path = DATABASE + ".tmp"
    try:
        folder = os.path.dirname(DATABASE)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        os.replace(temp_path, DATABASE)
        return True, ""
    except Exception as exc:
        return False, str(exc)

def money(value):
    try:
        return f"UGX {float(value):,.0f}"
    except:
        return "UGX 0"

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

class AnthoBizApp(App):
    def build(self):
        self.title = "AnthoBiz"
        self.data = load_database()
        self.root_layout = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))
        self.build_dashboard()
        return self.root_layout

    def show_message(self, title, message):
        body = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))
        label = Label(text=str(message), halign="left", valign="middle")
        label.bind(size=lambda inst, size: setattr(inst, "text_size", size))
        body.add_widget(label)
        close = Button(text="OK", size_hint_y=None, height=dp(48))
        body.add_widget(close)
        popup = Popup(title=title, content=body, size_hint=(0.9, 0.6))
        close.bind(on_release=popup.dismiss)
        popup.open()

    def make_button(self, text, height=56):
        return Button(text=text, size_hint_y=None, height=dp(height), font_size="16sp", background_normal="", background_color=(0.08, 0.35, 0.58, 1))

    def make_card(self, title, value, key):
        card = BoxLayout(orientation="vertical", padding=dp(8), spacing=dp(5), size_hint_y=None, height=dp(100))
        with card.canvas.before:
            Color(0.09, 0.16, 0.27, 1)
            rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(12)])
        card.bind(pos=lambda inst, pos: setattr(rect, "pos", pos), size=lambda inst, size: setattr(rect, "size", size))
        card.add_widget(Label(text=title, font_size="12sp", color=(0.65, 0.85, 1, 1)))
        card.add_widget(Label(text=str(value), font_size="16sp", bold=True))
        return card

    def build_dashboard(self):
        self.root_layout.clear_widgets()
        # --- MODERN HEADER WITH LOGO ---
        header = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(140), spacing=dp(4), padding=dp(4))
        if os.path.exists(LOGO_FILE):
            header.add_widget(Image(source=LOGO_FILE, size_hint_y=None, height=dp(95)))
        else:
            header.add_widget(Label(text="[b]ANTHOBIZ[/b]", markup=True, font_size="28sp", color=(0.2, 0.75, 1, 1), size_hint_y=None, height=dp(40)))
            header.add_widget(Label(text="ANTO-TECH SOLUTIONS", font_size="16sp", bold=True, color=(0.5, 0.85, 1, 1), size_hint_y=None, height=dp(22)))
        header.add_widget(Label(text=f"FIRMWARE • HARDWARE • ELECTRONICS • PROGRAMMING • CODING  |  v{APP_VERSION}", font_size="9sp", color=(0.6, 0.75, 0.9, 1), size_hint_y=None, height=dp(18)))
        self.root_layout.add_widget(header)
        
        scroll = ScrollView()
        content = BoxLayout(orientation="vertical", spacing=dp(10), size_hint_y=None)
        content.bind(minimum_height=content.setter("height"))
        content.add_widget(Label(text="[b]BUSINESS DASHBOARD[/b]", markup=True, font_size="20sp", size_hint_y=None, height=dp(42)))
        repairs = len(self.data["repairs"])
        products = sum(int(x.get("quantity", 0) or 0) for x in self.data["stock"] if isinstance(x, dict))
        revenue = sum(float(x.get("revenue", 0) or 0) for x in self.data["sales"] if isinstance(x, dict))
        expenses = sum(float(x.get("amount", 0) or 0) for x in self.data["expenses"] if isinstance(x, dict))
        cards = GridLayout(cols=2, spacing=dp(8), size_hint_y=None, height=dp(208))
        cards.add_widget(self.make_card("REPAIR JOBS", repairs, "repairs"))
        cards.add_widget(self.make_card("ITEMS IN STOCK", products, "stock"))
        cards.add_widget(self.make_card("SALES REVENUE", money(revenue), "revenue"))
        cards.add_widget(self.make_card("EXPENSES", money(expenses), "expenses"))
        content.add_widget(cards)
        content.add_widget(Label(text="[b]BUSINESS MANAGEMENT[/b]", markup=True, font_size="18sp", size_hint_y=None, height=dp(38)))
        for title, callback in [("Repairs", self.open_repairs), ("Inventory", self.open_inventory), ("Sales", self.open_sales), ("Expenses", self.open_expenses), ("Reports", self.open_reports), ("Backup", self.backup_database)]:
            btn = self.make_button(title)
            btn.bind(on_release=lambda instance, cb=callback: cb())
            content.add_widget(btn)
        content.add_widget(Label(text="Built by ANTO-TECH SOLUTIONS", size_hint_y=None, height=dp(38), font_size="12sp", color=(0.65, 0.75, 0.85, 1)))
        scroll.add_widget(content)
        self.root_layout.add_widget(scroll)

    def refresh_dashboard(self):
        self.data = load_database()
        self.build_dashboard()

    def commit_data(self):
        ok, error = save_database(self.data)
        if not ok:
            self.show_message("Save failed", error)
            return False
        return True

    def open_repairs(self):
        body = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(10))
        body.add_widget(Label(text="[b]REPAIR MANAGEMENT[/b]", markup=True, size_hint_y=None, height=dp(38), font_size="20sp"))
        for title, callback in [("Register New Repair", self.open_repair_form), ("View Repair Jobs", self.view_repairs)]:
            btn = self.make_button(title)
            btn.bind(on_release=lambda instance, cb=callback: cb())
            body.add_widget(btn)
        close = self.make_button("Close")
        body.add_widget(close)
        popup = Popup(title="AnthoBiz Repairs", content=body, size_hint=(0.92, 0.52))
        close.bind(on_release=popup.dismiss)
        popup.open()

    def open_repair_form(self):
        self.form_popup("Register Repair", [("Customer name", "customer"), ("Customer phone", "phone"), ("Device model", "device"), ("Reported problem", "problem"), ("Estimated cost (UGX)", "estimated"), ("Amount paid (UGX)", "paid")], [("Status", "status", STATUSES, "Pending")], "Save Repair Job", self.save_repair_form)

    def save_repair_form(self, values, popup):
        customer = values.get("customer", "").strip()
        device = values.get("device", "").strip()
        problem = values.get("problem", "").strip()
        if not customer or not device or not problem:
            self.show_message("Missing", "Enter customer, device and problem.")
            return
        try:
            estimated = float(values.get("estimated", "") or 0)
            paid = float(values.get("paid", "") or 0)
            if paid > estimated: raise ValueError
        except:
            self.show_message("Invalid", "Check amounts")
            return
        job = {"job_id": uuid.uuid4().hex[:10].upper(), "customer": customer, "phone": values.get("phone","").strip(), "device": device, "problem": problem, "estimated_cost": estimated, "amount_paid": paid, "balance": estimated-paid, "status": values.get("status","Pending"), "date": timestamp()}
        self.data["repairs"].append(job)
        if self.commit_data():
            popup.dismiss()
            self.refresh_dashboard()

    def view_repairs(self):
        if not self.data["repairs"]:
            self.show_message("Repair jobs", "No repair jobs yet.")
            return
        outer = BoxLayout(orientation="vertical", padding=dp(8), spacing=dp(8))
        scroll = ScrollView()
        listing = BoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None)
        listing.bind(minimum_height=listing.setter("height"))
        for job in reversed(self.data["repairs"]):
            card = BoxLayout(orientation="vertical", padding=dp(8), spacing=dp(4), size_hint_y=None, height=dp(245))
            details = f"[b]{job.get('customer','')}[/b]\nID: {job.get('job_id','')} . {job.get('date','')}\nPhone: {job.get('phone','')}\nDevice: {job.get('device','')}\nProblem: {job.get('problem','')}\nBalance: {money(job.get('balance',0))}"
            label = Label(text=details, markup=True, halign="left", valign="middle")
            label.bind(size=lambda inst, size: setattr(inst, "text_size", size))
            card.add_widget(label)
            row = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(6))
            spinner = Spinner(text=job.get("status","Pending"), values=STATUSES)
            update = Button(text="Update status")
            row.add_widget(spinner)
            row.add_widget(update)
            update.bind(on_release=lambda instance, jid=job.get("job_id"), sp=spinner: self.update_repair_status(jid, sp.text))
            card.add_widget(row)
            with card.canvas.before:
                Color(0.09, 0.16, 0.27, 1)
                rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(10)])
            card.bind(pos=lambda inst, pos: setattr(rect, "pos", pos), size=lambda inst, size: setattr(rect, "size", size))
            listing.add_widget(card)
        scroll.add_widget(listing)
        outer.add_widget(scroll)
        close = self.make_button("Close", 46)
        outer.add_widget(close)
        popup = Popup(title="Repair Records", content=outer, size_hint=(0.96, 0.9))
        close.bind(on_release=popup.dismiss)
        popup.open()

    def update_repair_status(self, job_id, status):
        job = next((x for x in self.data["repairs"] if x.get("job_id")==job_id), None)
        if job:
            job["status"] = status
            self.commit_data()

    def form_popup(self, title, field_specs, spinner_specs, save_text, save_callback):
        form = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(6), size_hint_y=None)
        form.bind(minimum_height=form.setter("height"))
        inputs = {}
        for label_text, key in field_specs:
            form.add_widget(Label(text=label_text, size_hint_y=None, height=dp(23), halign="left"))
            inp = TextInput(hint_text=label_text, multiline=False, size_hint_y=None, height=dp(42))
            form.add_widget(inp)
            inputs[key] = inp
        for label_text, key, options, default in spinner_specs:
            form.add_widget(Label(text=label_text, size_hint_y=None, height=dp(23)))
            spin = Spinner(text=default, values=options, size_hint_y=None, height=dp(42))
            form.add_widget(spin)
            inputs[key] = spin
        save = self.make_button(save_text, 48)
        form.add_widget(save)
        scroll = ScrollView()
        scroll.add_widget(form)
        popup = Popup(title=title, content=scroll, size_hint=(0.95, 0.9))
        save.bind(on_release=lambda instance: save_callback({k: w.text for k,w in inputs.items()}, popup))
        popup.open()
        return popup

    def open_inventory(self):
        body = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))
        add = self.make_button("Add product")
        view = self.make_button("View inventory")
        close = self.make_button("Close")
        body.add_widget(add)
        body.add_widget(view)
        body.add_widget(close)
        popup = Popup(title="Inventory", content=body, size_hint=(0.9, 0.48))
        add.bind(on_release=lambda *_: self.add_product())
        view.bind(on_release=lambda *_: self.view_inventory())
        close.bind(on_release=popup.dismiss)
        popup.open()

    def add_product(self):
        self.form_popup("Add Product", [("Product name", "name"), ("Quantity", "quantity"), ("Unit cost (UGX)", "cost"), ("Selling price (UGX)", "price")], [], "Save Product", self.save_product)

    def save_product(self, values, popup):
        name = values["name"].strip()
        if not name: return
        try:
            quantity = int(values["quantity"] or "0")
            cost = float(values["cost"] or "0")
            price = float(values["price"] or "0")
        except: return
        product = {"product_id": uuid.uuid4().hex[:10].upper(), "name": name, "quantity": quantity, "cost": cost, "price": price, "date": timestamp()}
        self.data["stock"].append(product)
        if self.commit_data():
            popup.dismiss()
            self.refresh_dashboard()

    def view_inventory(self):
        if not self.data["stock"]:
            self.show_message("Inventory", "No products yet.")
            return
        lines = [f"{i.get('name')}: {i.get('quantity')} units | Sell {money(i.get('price',0))}" for i in self.data["stock"]]
        self.show_message("Inventory", "\n\n".join(lines))

    def open_sales(self):
        body = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))
        record = self.make_button("Record sale")
        view = self.make_button("View sales")
        close = self.make_button("Close")
        body.add_widget(record)
        body.add_widget(view)
        body.add_widget(close)
        popup = Popup(title="Sales", content=body, size_hint=(0.9, 0.48))
        record.bind(on_release=lambda *_: self.record_sale())
        view.bind(on_release=lambda *_: self.view_sales())
        close.bind(on_release=popup.dismiss)
        popup.open()

    def record_sale(self):
        products = [x for x in self.data["stock"] if isinstance(x, dict)]
        if not products:
            self.show_message("No stock", "Add product first.")
            return
        names = [x.get("name") for x in products]
        form = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8), size_hint_y=None)
        form.bind(minimum_height=form.setter("height"))
        spinner = Spinner(text=names[0], values=names, size_hint_y=None, height=dp(44))
        qty_input = TextInput(hint_text="Quantity sold", input_filter="int", size_hint_y=None, height=dp(44))
        form.add_widget(spinner)
        form.add_widget(qty_input)
        save_btn = self.make_button("Save Sale", 48)
        form.add_widget(save_btn)
        scroll = ScrollView()
        scroll.add_widget(form)
        popup = Popup(title="Record Sale", content=scroll, size_hint=(0.9, 0.6))
        def do_save(instance):
            try:
                qty = int(qty_input.text or "0")
                prod = next((p for p in products if p.get("name")==spinner.text), None)
                if qty <=0 or qty > int(prod.get("quantity",0)):
                    self.show_message("Stock low", f"Only {prod.get('quantity')} left")
                    return
                prod["quantity"] -= qty
                revenue = qty * float(prod.get("price",0))
                sale = {"product": spinner.text, "quantity": qty, "revenue": revenue, "profit": revenue - qty*float(prod.get("cost",0)), "date": timestamp()}
                self.data["sales"].append(sale)
                if self.commit_data():
                    popup.dismiss()
                    self.refresh_dashboard()
            except: pass
        save_btn.bind(on_release=do_save)
        popup.open()

    def view_sales(self):
        if not self.data["sales"]:
            self.show_message("Sales", "No sales yet.")
            return
        lines = [f"{s.get('date')} | {s.get('product')} x{s.get('quantity')} = {money(s.get('revenue',0))}" for s in reversed(self.data["sales"])]
        self.show_message("Sales", "\n\n".join(lines[-20:]))

    def open_expenses(self):
        body = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))
        add = self.make_button("Add Expense")
        view = self.make_button("View Expenses")
        close = self.make_button("Close")
        body.add_widget(add)
        body.add_widget(view)
        body.add_widget(close)
        popup = Popup(title="Expenses", content=body, size_hint=(0.9, 0.48))
        add.bind(on_release=lambda *_: self.add_expense())
        view.bind(on_release=lambda *_: self.view_expenses())
        close.bind(on_release=popup.dismiss)
        popup.open()

    def add_expense(self):
        self.form_popup("Add Expense", [("Expense title", "title"), ("Amount (UGX)", "amount")], [], "Save Expense", self.save_expense)

    def save_expense(self, values, popup):
        try:
            amt = float(values.get("amount","") or 0)
            if amt <=0: return
        except: return
        exp = {"title": values.get("title","").strip(), "amount": amt, "date": timestamp()}
        self.data["expenses"].append(exp)
        if self.commit_data():
            popup.dismiss()
            self.refresh_dashboard()

    def view_expenses(self):
        if not self.data["expenses"]:
            self.show_message("Expenses", "No expenses yet.")
            return
        lines = [f"{e.get('date')} | {e.get('title')} = {money(e.get('amount',0))}" for e in reversed(self.data["expenses"])]
        self.show_message("Expenses", "\n\n".join(lines))

    def open_reports(self):
        total_sales = sum(float(x.get("revenue",0)) for x in self.data["sales"])
        total_profit = sum(float(x.get("profit",0)) for x in self.data["sales"])
        total_exp = sum(float(x.get("amount",0)) for x in self.data["expenses"])
        report = f"ANTHOBIZ REPORT v{APP_VERSION}\n{timestamp()}\n\nJobs: {len(self.data['repairs'])}\nStock Items: {len(self.data['stock'])}\nSales Revenue: {money(total_sales)}\nProfit: {money(total_profit)}\nExpenses: {money(total_exp)}\n\nNET: {money(total_profit-total_exp)}\n\nANTO-TECH SOLUTIONS"
        self.show_message("Reports", report)

    def backup_database(self):
        self.show_message("Backup", f"Backed up!\n{DATABASE}\nRepairs: {len(self.data['repairs'])} | Stock: {len(self.data['stock'])}\n\nAnto-Tech Solutions - All services")

if __name__ == "__main__":
    AnthoBizApp().run()
