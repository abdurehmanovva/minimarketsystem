#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os, time
from datetime import datetime

D, U = "data", "users.json"
P = "products.json"

def rj(f, d=None):
    try:
        with open(f, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except:
        return d if d is not None else {}

def wj(f, d):
    os.makedirs(D, exist_ok=True)
    with open(f, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2)

def ap(f, l):
    os.makedirs(D, exist_ok=True)
    with open(f, "a", encoding="utf-8") as fh:
        fh.write(l + "\n")

def lg(u, e, x=""):
    ap(os.path.join(D, f"history_{u}.log"), f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {e}" + (f" {x}" if x else ""))

def init():
    os.makedirs(D, exist_ok=True)
    if not os.path.exists(os.path.join(D, U)):
        wj(os.path.join(D, U), [
            {"username": "student1", "password": "1234", "balance": 100.0, "failed": 0, "lock": None},
            {"username": "student2", "password": "abcd", "balance": 250.0, "failed": 0, "lock": None}
        ])
    if not os.path.exists(os.path.join(D, P)):
        wj(os.path.join(D, P), {
            "Geyimlər": [{"id": 1, "name": "T-Shirt", "price": 12.5}, {"id": 2, "name": "Hoodie", "price": 45}, {"id": 3, "name": "Jeans", "price": 60}, {"id": 4, "name": "Köynək", "price": 35}],
            "Elektronika": [{"id": 1, "name": "Qulaqlıq", "price": 35}, {"id": 2, "name": "Powerbank", "price": 25}, {"id": 3, "name": "Siçan", "price": 15}, {"id": 4, "name": "Klaviatura", "price": 55}],
            "Kitablar": [{"id": 1, "name": "Algorithms 101", "price": 20}, {"id": 2, "name": "Clean Code", "price": 55}, {"id": 3, "name": "Python Basics", "price": 30}, {"id": 4, "name": "Data Structures", "price": 40}],
            "Aksesuarlar": [{"id": 1, "name": "Saat", "price": 80}, {"id": 2, "name": "Kəmər", "price": 18}, {"id": 3, "name": "Cüzdan", "price": 25}, {"id": 4, "name": "Eynək", "price": 45}]
        })

def gusr():
    return rj(os.path.join(D, U), [])

def susr(v):
    wj(os.path.join(D, U), v)

def fusr(n):
    for u in gusr():
        if u["username"] == n:
            return u
    return None

def uusr(n, k):
    v = gusr()
    for u in v:
        if u["username"] == n:
            u.update(k)
            break
    susr(v)

def lk(u):
    return u.get("lock") and time.time() < u["lock"]

def cd(n):
    for i in range(n, 0, -1):
        print(f"\r  [⏳] Gözləyin: {i}s ", end="", flush=True)
        time.sleep(1)
    print("\r  [✓] Yenidən cəhd edə bilərsiniz!      ")

def login():
    while True:
        print("\n" + "=" * 50 + "\n  MINI MAGAZA - GIRIS\n" + "=" * 50)
        n = input("\n  Istifadəçi: ").strip()
        u = fusr(n)
        if not u:
            print("  [X] Istifadəçi tapılmadı!")
            if input("  Yenidən? (h/e): ").lower() == "e":
                return None
            continue
        if lk(u):
            r = int(u["lock"] - time.time())
            print(f"  [X] Bloklu! {r}s gözləyin.")
            cd(r)
            uusr(n, {"failed": 0, "lock": None})
            u = fusr(n)
        a = 3 - u.get("failed", 0)
        while a > 0:
            p = input(f"  Parol ({a} cəhd): ").strip()
            if p == u["password"]:
                uusr(n, {"failed": 0, "lock": None})
                lg(n, "LOGIN_SUCCESS")
                print(f"\n  [✓] Xoş gəldiniz, {n}!")
                return fusr(n)
            a -= 1
            uusr(n, {"failed": u.get("failed", 0) + 1})
            u = fusr(n)
            print(f"  [X] Yanlış!")
            lg(n, "LOGIN_FAIL")
            if a == 0:
                l = time.time() + 10
                uusr(n, {"lock": l})
                lg(n, "LOGIN_FAIL", "→ COOLDOWN 10s")
                print(f"\n  [⚠] 3 səhv! 10s cooldown.")
                cd(10)
                uusr(n, {"failed": 0, "lock": None})
                break

def prd():
    return rj(os.path.join(D, P), {})

def fp(c, i):
    for p in prd().get(c, []):
        if p["id"] == i:
            return p
    return None

def bsk(u):
    return rj(os.path.join(D, f"basket_{u}.json"), [])

def wbs(u, v):
    wj(os.path.join(D, f"basket_{u}.json"), v)

def fav(u):
    return rj(os.path.join(D, f"favorites_{u}.json"), [])

def wfv(u, v):
    wj(os.path.join(D, f"favorites_{u}.json"), v)

def shb(u):
    b = bsk(u)
    if not b:
        print("\n[ℹ] Səbət boşdur."); return
    print(f"\n{'='*60}\n  SƏBƏT\n{'-'*60}\n  {'#':<4}{'Kateqoriya':<14}{'Məhsul':<18}{'Vahid':<8}{'Ədəd':<6}{'Cəmi':<8}")
    t = 0
    for i, x in enumerate(b, 1):
        print(f"  {i:<4}{x['category']:<14}{x['product']:<18}{x['unit']:<8.2f}{x['qty']:<6}{x['line_total']:<8.2f}")
        t += x["line_total"]
    print(f"{'-'*60}\n  {'ÜMUMI:':<50}{t:>8.2f} AZN\n{'='*60}")

def adb(u, c, p, q):
    b = bsk(u)
    for x in b:
        if x["category"] == c and x["product"] == p["name"]:
            x["qty"] += q
            x["line_total"] = x["unit"] * x["qty"]
            wbs(u, b)
            lg(u, "BASKET_ADD", f"({c}/{p['name']} x{q})")
            print(f"\n  [✓] Əlavə edildi! (Cəmi: {x['qty']})"); return
    b.append({"category": c, "product": p["name"], "unit": p["price"], "qty": q, "line_total": p["price"] * q})
    wbs(u, b)
    lg(u, "BASKET_ADD", f"({c}/{p['name']} x{q})")
    print(f"\n  [✓] Səbətə əlavə edildi!")

def chout(u):
    b = bsk(u)
    if not b:
        print("\n[ℹ] Səbət boşdur."); return
    t = sum(x["line_total"] for x in b)
    us = fusr(u)
    bl = us["balance"]
    print(f"\n{'='*50}\n  CHECKOUT\n{'-'*50}\n  Cəmi: {t:.2f} AZN\n  Balans: {bl:.2f} AZN\n{'-'*50}")
    if bl >= t:
        nb = bl - t
        uusr(u, {"balance": nb})
        ps = rj(os.path.join(D, f"purchases_{u}.json"), [])
        ps.append({"ts": datetime.now().isoformat(), "items": b, "total": t})
        wj(os.path.join(D, f"purchases_{u}.json"), ps)
        wbs(u, [])
        lg(u, "CHECKOUT_SUCCESS", f"total={t:.2f} | {bl:.2f} → {nb:.2f}")
        print(f"  [✓] Alış tamamlandı!\n  [✓] Balans: {bl:.2f} → {nb:.2f} AZN")
    else:
        lg(u, "CHECKOUT_FAIL", f"(insufficient) need={t:.2f} have={bl:.2f}")
        print(f"  [X] Balans çatışmaz! {t - bl:.2f} AZN çatışmır.\n  [ℹ] Səbət saxlanıldı.")
    print(f"{'='*50}")

def shf(u):
    f = fav(u)
    if not f:
        print("\n[ℹ] Favorit boşdur."); return
    print(f"\n{'='*50}\n  FAVORITLƏR\n{'-'*50}\n  {'#':<4}{'Kateqoriya':<14}{'Məhsul':<18}{'Qiymət':<8}")
    for i, x in enumerate(f, 1):
        print(f"  {i:<4}{x['category']:<14}{x['name']:<18}{x['price']:<8.2f}")
    print(f"{'='*50}\n  add <id> → Səbət | remove <id> → Sil | back")

def adf(u, c, p):
    f = fav(u)
    for x in f:
        if x["category"] == c and x["name"] == p["name"]:
            print("\n  [ℹ] Artıq favoritdədir."); return
    f.append({"category": c, "id": p["id"], "name": p["name"], "price": p["price"]})
    wfv(u, f)
    lg(u, "FAVORITE_ADD", f"({c}/{p['name']})")
    print(f"\n  [✓] Favoritə əlavə edildi!")

def shh(u):
    f = os.path.join(D, f"history_{u}.log")
    if not os.path.exists(f):
        print("\n[ℹ] Tarixçə boşdur."); return
    with open(f, "r", encoding="utf-8") as fh:
        l = [x.strip() for x in fh if x.strip()]
    print(f"\n{'='*60}\n  TARIXÇƏ (son {min(20, len(l))})\n{'='*60}")
    for x in l[-20:]:
        print(f"  {x}")
    print(f"{'='*60}")

def chp(u):
    print(f"\n{'='*50}\n  SETTINGS - ŞIFRƏ DƏYIŞMƏ\n{'='*50}")
    o = input("  Köhnə şifrə: ").strip()
    if o != fusr(u)["password"]:
        print("  [X] Yanlış köhnə şifrə!"); lg(u, "PASSWORD_CHANGE_FAIL"); return
    n = input("  Yeni şifrə (min 4): ").strip()
    if len(n) < 4:
        print("  [X] Min 4 simvol!"); return
    if input("  Təkrar: ").strip() != n:
        print("  [X] Uyğun gəlmir!"); return
    uusr(u, {"password": n})
    lg(u, "PASSWORD_CHANGED")
    print(f"\n  [✓] Şifrə dəyişdirildi!\n{'='*50}")

def catm(u):
    pd = prd()
    while True:
        cats = list(pd.keys())
        print(f"\n{'='*50}\n  KATEQORİYALAR\n{'='*50}")
        for i, c in enumerate(cats, 1):
            print(f"  {i}) {c}")
        print("  0) Geri\n" + "=" * 50)
        ch = input("  Seçim: ").strip()
        if ch == "0":
            return
        try:
            c = cats[int(ch) - 1]
            prodm(u, pd, c)
        except:
            print("  [X] Yanlış!")

def prodm(u, pd, c):
    while True:
        it = pd.get(c, [])
        if not it:
            print("  [ℹ] Boş!"); return
        print(f"\n{'='*50}\n  {c.upper()}\n{'-'*50}\n  {'ID':<5}{'Ad':<22}{'Qiymət':>10}")
        for p in it:
            print(f"  {p['id']:<5}{p['name']:<22}{p['price']:>10.2f}")
        print(f"{'='*50}")
        ch = input("\n  ID (0=Geri): ").strip()
        if ch == "0":
            return
        try:
            p = fp(c, int(ch))
            if not p:
                print("  [X] Tapılmadı!"); continue
            print(f"\n  {'='*40}\n  {p['name']} - {p['price']:.2f} AZN\n  {'='*40}")
            q = input("  Miqdar: ").strip()
            try:
                q = int(q)
                if q <= 0:
                    print("  [X] Müsbət ədəd!"); continue
            except:
                print("  [X] Yanlış!"); continue
            a = input("  [B]Səbət [F]Favorit [X]Ləğv: ").strip().upper()
            if a == "B":
                adb(u, c, p, q)
            elif a == "F":
                adf(u, c, p)
            elif a == "X":
                print("  [ℹ] Ləğv.")
            input("\n  Enter...")
        except:
            print("  [X] Yanlış!")

def bskm(u):
    while True:
        shb(u)
        print("  list | qty <id> <miq> | remove <id> | clear | checkout | back")
        c = input("\n  Əmr: ").strip().lower().split()
        if not c:
            continue
        if c[0] == "back":
            return
        elif c[0] == "list":
            continue
        elif c[0] == "clear":
            wbs(u, []); lg(u, "BASKET_CLEAR"); print("  [✓] Təmizləndi.")
        elif c[0] == "checkout":
            chout(u)
        elif c[0] == "qty" and len(c) == 3:
            try:
                b = bsk(u)
                i = int(c[1]) - 1
                q = int(c[2])
                if 0 <= i < len(b) and q > 0:
                    b[i]["qty"] = q
                    b[i]["line_total"] = b[i]["unit"] * q
                    wbs(u, b)
                    lg(u, "BASKET_QTY", f"({b[i]['product']} → {q})")
                    print("  [✓] Yeniləndi.")
                else:
                    print("  [X] Yanlış!")
            except:
                print("  [X] Yanlış!")
        elif c[0] == "remove" and len(c) == 2:
            try:
                b = bsk(u)
                i = int(c[1]) - 1
                if 0 <= i < len(b):
                    lg(u, "BASKET_REMOVE", f"({b.pop(i)['product']})")
                    wbs(u, b)
                    print("  [✓] Silindi.")
                else:
                    print("  [X] Yanlış!")
            except:
                print("  [X] Yanlış!")
        else:
            print("  [X] Yanlış əmr!")
        input("\n  Enter...")

def fvm(u):
    while True:
        shf(u)
        c = input("\n  Əmr: ").strip().lower().split()
        if not c:
            continue
        if c[0] == "back":
            return
        elif c[0] == "remove" and len(c) == 2:
            try:
                f = fav(u)
                i = int(c[1]) - 1
                if 0 <= i < len(f):
                    lg(u, "FAVORITE_REMOVE", f"({f.pop(i)['name']})")
                    wfv(u, f)
                    print("  [✓] Silindi.")
                else:
                    print("  [X] Yanlış!")
            except:
                print("  [X] Yanlış!")
        elif c[0] == "add" and len(c) == 2:
            try:
                f = fav(u)
                i = int(c[1]) - 1
                if 0 <= i < len(f):
                    x = f[i]
                    q = input(f"  {x['name']} üçün miqdar: ").strip()
                    q = int(q)
                    if q > 0:
                        adb(u, x["category"], {"name": x["name"], "price": x["price"]}, q)
                    else:
                        print("  [X] Müsbət!")
                else:
                    print("  [X] Yanlış!")
            except:
                print("  [X] Yanlış!")
        else:
            print("  [X] Yanlış əmr!")
        input("\n  Enter...")

def main():
    init()
    print("\n" + "=" * 50 + "\n  MINI MAGAZA SISTEMI\n" + "=" * 50)
    u = login()
    if not u:
        return
    n = u["username"]
    while True:
        print(f"\n{'='*50}\n  MENYU [{n}]\n{'='*50}\n  1)Kateqoriyalar  2)Səbət  3)Favorit\n  4)Tarixçə  5)Settings  6)Balans  0)Çıxış\n{'='*50}")
        ch = input("  Seçim: ").strip()
        if ch == "1":
            catm(n)
        elif ch == "2":
            bskm(n)
        elif ch == "3":
            fvm(n)
        elif ch == "4":
            shh(n); input("\n  Enter...")
        elif ch == "5":
            chp(n); input("\n  Enter...")
        elif ch == "6":
            print(f"\n{'='*40}\n  BALANS: {fusr(n)['balance']:.2f} AZN\n{'='*40}"); input("\n  Enter...")
        elif ch == "0":
            print(f"\n  [✓] Sağ olun, {n}!"); lg(n, "LOGOUT"); break
        else:
            print("  [X] Yanlış!")

if __name__ == "__main__":
    main()