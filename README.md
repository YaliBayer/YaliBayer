<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&amp;height=220&amp;color=0:1c1b18,100:2b4bff&amp;text=Yali%20Tal&amp;fontColor=f5f3ef&amp;fontSize=58&amp;fontAlignY=38&amp;desc=Infrastructure%20%26%20Electronics&amp;descAlignY=58&amp;descSize=18" alt="Yali Tal - Infrastructure and Electronics" width="100%" />

<br />

<a href="https://www.yali.website">
  <img src="https://img.shields.io/badge/website-yali.website-2b4bff?style=for-the-badge&amp;labelColor=1c1b18" alt="Website" />
</a>
<a href="https://www.yali.website/download_resume/">
  <img src="https://img.shields.io/badge/download-live_pdf-f5f3ef?style=for-the-badge&amp;labelColor=1c1b18&amp;color=7a7568" alt="Download live PDF" />
</a>
<img src="https://img.shields.io/badge/built_with-Django-0C4B33?style=for-the-badge&amp;labelColor=1c1b18" alt="Built with Django" />
<img src="https://img.shields.io/badge/deployed_on-Vercel-000000?style=for-the-badge&amp;labelColor=1c1b18" alt="Deployed on Vercel" />

<br />
<br />

<strong>A builder at heart.</strong><br />
Navigating the intersection of hardware modding, network defense, and self-hosted systems.

</div>

---

## Snapshot

```text
yali@homelab:~$ whoami
Infrastructure-minded builder, SOC analyst, hardware tinkerer.

yali@homelab:~$ current-focus
Network defense | Linux servers | Docker | ESPHome | practical electronics

yali@homelab:~$ philosophy
If I cannot explain how it works, I have not earned the right to run it.
```

## Experience

<table>
  <tr>
    <td width="28%"><strong>Cyber Security Analyst</strong><br /><sub>IDF · ongoing</sub></td>
    <td>
      Junior SOC analyst focused on real-time network monitoring, vulnerability identification,
      and maintaining digital infrastructure integrity. The work has sharpened my operational
      discipline, incident response instincts, and understanding of the technical why behind defense.
    </td>
  </tr>
  <tr>
    <td><strong>Service &amp; Operations</strong><br /><sub>Niro Cafe · 2022-2024</sub></td>
    <td>
      Running a busy cafe floor taught me to stay calm when everything goes sideways at once.
      Turns out that skill travels well.
    </td>
  </tr>
</table>

## Projects

<table>
  <tr>
    <td width="33%">
      <h3>The NFC Jukebox</h3>
      <p><code>ESP32 / IoT</code></p>
      <p>Tap a card, play an album. RC522 reader, ESPHome, Home Assistant, MQTT, and Spotify automation.</p>
    </td>
    <td width="33%">
      <h3>Homelab Architecture</h3>
      <p><code>Linux / Docker</code></p>
      <p>Private cloud at home: Immich, AdGuard, containerised services, and a lot of learning through breakage.</p>
    </td>
    <td width="33%">
      <h3>Horology &amp; Modding</h3>
      <p><code>Hardware precision</code></p>
      <p>Custom NH35 movement assembly and regulation. Tiny tolerances, patient hands, practical electronics mindset.</p>
    </td>
  </tr>
</table>

## Stack

<p>
  <img src="https://img.shields.io/badge/Ubuntu_Server-E95420?style=flat-square&amp;logo=ubuntu&amp;logoColor=white" alt="Ubuntu Server" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&amp;logo=docker&amp;logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/ESPHome-000000?style=flat-square&amp;logo=esphome&amp;logoColor=white" alt="ESPHome" />
  <img src="https://img.shields.io/badge/Home_Assistant-41BDF5?style=flat-square&amp;logo=homeassistant&amp;logoColor=white" alt="Home Assistant" />
  <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&amp;logo=django&amp;logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/Vercel-000000?style=flat-square&amp;logo=vercel&amp;logoColor=white" alt="Vercel" />
  <img src="https://img.shields.io/badge/PC_Assembly-2b4bff?style=flat-square" alt="PC Assembly" />
  <img src="https://img.shields.io/badge/Soldering-7a7568?style=flat-square" alt="Soldering" />
</p>

## How The Resume PDF Works

The download endpoint does not serve a stale file. It renders the website template, extracts the resume content, and generates a styled PDF on demand.

```mermaid
flowchart LR
    A[resume.html] --> B[content parser]
    B --> C[PDF layout engine]
    C --> D[/download_resume/]
    D --> E[Fresh PDF]
```

## Repository Map

```text
core/
  templates/resume.html   website resume content
  views.py                homepage and download route
  pdf.py                  dynamic styled PDF generator
resume_project/
  settings.py             Django settings
  urls.py                 URL routes
vercel.json               Vercel deployment config
```

## Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/download_resume/
```

---

<div align="center">

<sub>built with curiosity</sub>

<br />
<br />

<img src="https://capsule-render.vercel.app/api?type=waving&amp;height=90&amp;section=footer&amp;color=0:2b4bff,100:1c1b18" alt="" width="100%" />

</div>
