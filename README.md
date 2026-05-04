Fayl Əsaslı Mini Mağaza Sistemi

### Quraşdırma və İşə salma

> **Qeyd:** İlk işə salınmada `data/` qovluğu və default fayllar avtomatik yaradılacaq.

## 📑 Menyu Strukturu

### Login Ekranı
```
İstifadəçi adı: ______
Parol (3 cəhd qalıb): ______
```

### Əsas Menyu
```
1) Kateqoriyalar
2) Səbətim
3) Favoritlərim
4) Tarixçə
5) Settings (şifrəni dəyiş)
6) Balansımı göstər
0) Çıxış
```

### Kateqoriyalar → Məhsullar
```
1) Geyimlər
2) Elektronika
3) Kitablar
4) Aksesuarlar
0) Geri
```

### Məhsul Detalı
```
Məhsul: T-Shirt
Qiymət: 12.50 AZN
Miqdar (ədəd): 2

Əməliyyat: [B] Səbətə | [F] Favorit | [X] Ləğv
```

### Səbət Menyusu
```
list              → Səbəti göstər
qty <id> <miqdar> → Miqdarı dəyiş
remove <id>       → Sətri sil
clear             → Səbəti təmizlə
checkout          → Alışı tamamla
back              → Geri
```

---

## 📁 Fayl Formatları

### `users.json`
```json
[
  {
    "username": "student1",
    "password": "1234",
    "balance": 100.0,
    "failed_attempts": 0,
    "lock_until": null
  }
]
```

### `products.json`
```json
{
  "Geyimlər": [
    {"id": 1, "name": "T-Shirt", "price": 12.50},
    {"id": 2, "name": "Hoodie", "price": 45.00}
  ],
  "Elektronika": [
    {"id": 1, "name": "Qulaqlıq", "price": 35.00}
  ]
}
```

### `basket_<username>.json`
```json
[
  {
    "category": "Geyimlər",
    "product": "T-Shirt",
    "unit": 12.50,
    "qty": 2,
    "line_total": 25.00
  }
]
```

### `purchases_<username>.json`
```json
[
  {
    "ts": "2025-10-25T13:25:40",
    "items": [...],
    "total": 60.00
  }
]
```

### `favorites_<username>.json`
```json
[
  {"category": "Geyimlər", "id": 2, "name": "Hoodie", "price": 45.00}
]
```

### `history_<username>.log`
```
[2025-10-25 13:18:01] LOGIN_FAIL (wrong password)
[2025-10-25 13:18:09] LOGIN_FAIL (wrong password) → COOLDOWN 10s
[2025-10-25 13:18:20] LOGIN_SUCCESS (istifadəçi: student1)
[2025-10-25 13:20:12] BASKET_ADD (Geyimlər/T-Shirt x2)
[2025-10-25 13:24:10] CHECKOUT_SUCCESS total=60.00 | balance: 100.00 → 40.00
```

---

## ⚙️ Funksionallıq

| Xüsusiyyət | Təsvir |
|------------|--------|
| **Login** | Username + password ilə giriş |
| **Cooldown** | 3 səhv cəhd → 10 saniyə gözləmə + geri sayım taymeri |
| **Kateqoriyalar** | 4 kateqoriya, hərində 4 məhsul |
| **Səbət** | Əlavə, miqdar dəyişmə, silmə, təmizləmə, checkout |
| **Checkout** | Balans yoxlanışı, uğurlu/uğursuz qeyd |
| **Favoritlər** | Əlavə, silmə, səbətə köçürmə |
| **Settings** | Köhnə şifrə təsdiqi ilə yeni şifrə (min. 4 simvol) |
| **Tarixçə** | Son 20 hadisənin log faylında saxlanması |
| **Balans** | Real-time balans göstəricisi |
| **Persistensiya** | Bütün məlumatlar JSON fayllarda saxlanılır |

---

## 🧪 Test Ssenariləri

### Ssenari 1: Uğurlu Alış Axını
1. Login: `student1` / `1234`
2. Kateqoriyalar → Geyimlər → T-Shirt (ID: 1)
3. Miqdar: 2 → **B** (Səbətə)
4. Kateqoriyalar → Elektronika → Qulaqlıq (ID: 1)
5. Miqdar: 1 → **B** (Səbətə)
6. Səbətim → `checkout`
7. Balans: 100.00 → 27.50 AZN

### Ssenari 2: Login Limiti + Cooldown
1. Login: `student1` / `wrong1` → Fail
2. Login: `student1` / `wrong2` → Fail
3. Login: `student1` / `wrong3` → Fail → **10s cooldown**
4. Taymer bitdikdən sonra: `student1` / `1234` → Success

### Ssenari 3: Favorit → Səbət → Checkout
1. Login: `student1` / `1234`
2. Kateqoriyalar → Kitablar → Clean Code
3. Miqdar: 1 → **F** (Favorit)
4. Favoritlərim → `add 1` → Miqdar: 1
5. Səbətim → `checkout`

### Ssenari 4: Uğursuz Checkout
1. Login: `student1` / `1234`
2. Kateqoriyalar → Aksesuarlar → Saat (80 AZN)
3. Miqdar: 2 → **B** (Səbətə)
4. Səbətim → `checkout` → **Rədd** (160 > 100)


## 📝 Qeydlər

- Bütün fayllar proqram tərəfindən avtomatik yaradılır.
- Fayl formatı pozulsa, default dəyərlərlə yenidən yaradılır.
- Miqdar yalnız müsbət tam ədəd qəbul olunur.
- Səbətdə eyni məhsul varsa, miqdar artırılır (duplikat yaradılmır).
- Balans kifayət etmədikdə checkout rədd edilir və səbət saxlanılır.