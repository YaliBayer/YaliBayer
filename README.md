<div align="center">

<p><strong>Infrastructure & Electronics</strong></p>

# Yali Tal

Builder at heart. Navigating the intersection of hardware modding, network defense, and self-hosted systems.

[Visit the Website](https://www.yali.website) · [Download the Live PDF](https://www.yali.website/download_resume/)

</div>

---

## Experience

### Cyber Security Analyst (SOC)

`IDF · ongoing`

Serving as a Junior Analyst within a military Security Operations Center. My role focuses on real-time network monitoring, identifying system vulnerabilities, and maintaining the integrity of digital infrastructure. This service has taught me operational discipline, rapid incident response, and the technical why behind network defense.

### Service & Operations

`Niro Cafe · 2022-2024`

Running a busy cafe floor teaches you to stay calm when everything goes sideways at once. Turns out that is a useful skill everywhere else too.

---

## Projects

### The NFC Jukebox

`ESP32 / IoT`

Tap a card, play an album. Physical media for the streaming age: RC522 reader, ESPHome, Home Assistant, MQTT, and Spotify automation.

### Homelab Architecture

`Linux / Docker`

Private cloud at home. Immich for photos, AdGuard for DNS, containerised everything. Breaks more than I would like. I learn every time it does.

### Horology & Modding

`Hardware precision`

Custom NH35 movement assembly and regulation. Patience-intensive, tolerance-unforgiving, and good practice for electronics work generally.

---

## Stack

`Ubuntu Server` `Docker` `ESPHome` `Home Assistant` `PC Assembly` `Soldering` `Hebrew` `English`

---

## About This Site

This repository powers my personal resume website, built with Django and deployed on Vercel.

The PDF download is generated dynamically from the website template. That means when the resume content changes on the site, the next PDF download is generated from the updated page instead of serving an old static file.

```text
Website template  ->  resume content parser  ->  styled PDF generator  ->  download
```

### Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/download_resume/
```

---

<div align="center">

built with curiosity · Jerusalem

</div>
