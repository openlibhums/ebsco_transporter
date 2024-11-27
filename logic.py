import os
import shutil
import logging

from janeway_ftp import sftp, helpers as deposit_helpers

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
from core import files

from journal import models


def get_issue_from_id(issue_id):
    return get_object_or_404(
        models.Issue,
        pk=issue_id,
    )


def download_issue(issue_id):
    issue = get_issue_from_id(issue_id)
    temp_folder = make_temp_folder(issue)
    try:
        issue_zip_path = prep_and_zip_issue(issue, temp_folder)
        return files.serve_temp_file(
            issue_zip_path,
            f"{issue.journal.code}_{issue.volume}_{issue.issue}_{issue.date.year}_{timezone.now().strftime('%Y-%m-%d')}.zip",
        )
    finally:
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder, ignore_errors=True)


def transport_issue(issue_id):
    issue = get_issue_from_id(issue_id)
    temp_folder = make_temp_folder(issue)
    try:
        issue_zip_path = prep_and_zip_issue(issue, temp_folder)
        upload_issue_zip(
            issue_zip_path,
            os.path.basename(issue_zip_path),
        )
    finally:
        if os.path.exists(temp_folder):
            shutil.rmtree(temp_folder, ignore_errors=True)


def upload_issue_zip(zip_path, file_name,):
    try:
        sftp.send_file_via_sftp(
            ftp_server=settings.EBSCO_FTP_SERVER,
            ftp_username=settings.EBSCO_FTP_USERNAME,
            ftp_password=settings.EBSCO_FTP_PASSWORD,
            remote_file_path='',
            file_path=zip_path,
            file_name=file_name,
        )
        logging.info(f"Uploaded {file_name}")
    except Exception as e:
        logging.error(
            f"Failed to upload {file_name}: {e}",
        )
        raise


def prep_and_zip_issue(issue, temp_folder):
    issue_folder = os.path.join(temp_folder, str(issue.pk))
    os.makedirs(issue_folder, exist_ok=True)

    # Add each article as a folder with XML inside the issue folder
    for article_data in issue.issue_articles:
        article = article_data.get('article')
        if article:
            add_article_to_package(article, issue_folder)
        else:
            logging.warning(f"Skipped invalid article entry: {article_data}")

    # Create a single zip for the issue
    zip_name = f"{issue.journal.code}_{issue.volume}_{issue.issue}_{issue.date.year}_{timezone.now().strftime('%Y-%m-%d')}"
    zip_path = shutil.make_archive(
        base_name=os.path.join(temp_folder, zip_name),
        format='zip',
        root_dir=issue_folder,
    )
    return zip_path


def make_temp_folder(issue):
    base_temp_dir = os.path.join('files', 'temp', 'deposit')
    folder_name = f"temp_{timezone.now().strftime('%Y%m%d%H%M%S')}"
    temp_folder = os.path.join(base_temp_dir, folder_name)
    os.makedirs(temp_folder, exist_ok=True)
    return temp_folder


def add_article_to_package(article, issue_folder):
    article_folder = os.path.join(issue_folder, str(article.pk))
    files.mkdirs(article_folder)

    galleys = article.galley_set.all()
    xml_galley = deposit_helpers.get_best_deposit_xml_galley(article, galleys)
    if xml_galley:
        try:
            files.copy_file_to_folder(
                xml_galley.file.self_article_path(),
                xml_galley.file.uuid_filename,
                article_folder,
            )
            for image in xml_galley.images.all():
                files.copy_file_to_folder(
                    image.self_article_path(),
                    image.original_filename,
                    article_folder,
                )
        except FileNotFoundError:
            deposit_helpers.generate_jats_metadata(
                article,
                article_folder,
            )
    else:
        deposit_helpers.generate_jats_metadata(
            article,
            article_folder,
        )


def zip_article(article_folder, article):
    zip_name = f"{article.pk}"
    zip_path = shutil.make_archive(
        base_name=os.path.join(os.path.dirname(article_folder), zip_name),
        format='zip',
        root_dir=article_folder,
    )
    return zip_path
