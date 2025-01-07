# EBSCO Transporter

An FTP plugin for depositing works with EBSCO.

## Install

1. Clone this repository into your path/to/janeway/src/plugins/ folder
2. Checkout a version that will work with your current Janeway version
3. Install requirements (check if you're using a virtualenv) with pip3 install -r `requirements.txt`
4. Add settings (detailed below) to `settings.py`
5. Install the plugin with `python3 src/manage.py install_plugins so_transporter
6. Restart your server

## Settings

The following settings should be added to your `settings.py` file.

```python
EBSCO_FTP_SERVER = 'a.server.com'
EBSCO_FTP_USERNAME = 'ausername'
EBSCO_FTP_PASSWORD = 'apassword'
```

## How it works

Deposits a zip file of articles on EBSCO's FTP server. The zip packages are in the following format:

- ** Issue Zip **
  - Art 1 JATS (either XML galley or stub)
  - Art 2 JATS
  - ...

