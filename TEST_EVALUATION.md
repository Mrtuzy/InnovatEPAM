# Evaluation Endpoint Test Guide

## Problem
"Failed to submit evaluation. Please try again." hatası alınıyor.

## Debug Adımları

### 1. Browser Console'u Kontrol Et (ÖNEMLİ!)
1. http://localhost:3001 adresine git
2. F12 tuşuna bas (Developer Tools)
3. **Console** sekmesine geç
4. Evaluation göndermeyi dene
5. Console'da görünen tüm hataları not et

### 2. Network Tab'ı Kontrol Et
1. Developer Tools'da **Network** sekmesine geç  
2. Evaluation göndermeyi dene
3. `evaluate` isteğini bul
4. İsteğe tıkla ve şunları kontrol et:
   - **Request URL**: `/api/v1/ideas/{id}/evaluate` şeklinde olmalı
   - **Request Method**: POST olmalı
   - **Status Code**: Ne döndüğünü kontrol et
   - **Headers**: Authorization header var mı?
   - **Response**: Backend'den gelen hata mesajını oku

### 3. Backend Log Kontrolü
Terminal'de backend çalışıyorsa hataları göreceksiniz.

### 4. Manuel API Testi (PowerShell)

Admin olarak giriş yap ve token al:
```powershell
$loginResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/login" -Method POST -Body (@{
    email = "admin@example.com"
    password = "admin123"
} | ConvertTo-Json) -ContentType "application/json"

$token = $loginResponse.access_token
Write-Host "Token: $token"
```

Bir idea ID'si bul:
```powershell
$ideas = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/ideas/my-ideas" -Headers @{
    Authorization = "Bearer $token"
}
$ideaId = $ideas.items[0].id
Write-Host "Idea ID: $ideaId"
```

Evaluation gönder:
```powershell
$evalResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/ideas/$ideaId/evaluate" -Method POST -Headers @{
    Authorization = "Bearer $token"
    "Content-Type" = "application/json"
} -Body (@{
    new_status = "under_review"
    comment = "This is a test evaluation comment with more than 10 characters"
} | ConvertTo-Json)

Write-Host "Success! Evaluation created:"
$evalResponse | ConvertTo-Json -Depth 3
```

## Olası Sorunlar ve Çözümler

### 1. 401 Unauthorized
- **Sebep**: Token geçersiz veya eksik
- **Çözüm**: Logout yapıp tekrar login ol

### 2. 403 Forbidden  
- **Sebep**: Admin değilsin
- **Çözüm**: Admin hesabıyla giriş yap (admin@example.com / admin123)

### 3. 404 Not Found
- **Sebep**: Endpoint bulunamadı
- **Çözüm**: Backend'i yeniden başlat

### 4. 400 Bad Request
- **Sebep**: 
  - Yorum çok kısa (< 10 kar)
  - Aynı status'a geçiş yapılıyor
  - Geçersiz status
- **Çözüm**: Form validasyonlarını kontrol et

### 5. CORS Error
- **Sebep**: Frontend-Backend arası CORS ayarı yanlış
- **Çözüm**: Backend'in CORS ayarlarını kontrol et

## Güncel Durum

- ✅ Backend çalışıyor: Port 8000
- ✅ Frontend çalışıyor: Port 3001  
- ✅ Evaluation model var
- ✅ Evaluation repository var
- ✅ Evaluation endpoint'leri var
- ✅ Frontend component'leri var
- ⚠️ Error handling geliştirildi (daha detaylı console log)

## Sonraki Adım

Browser console'u kontrol et ve çıkan hatayı bana ilet!
