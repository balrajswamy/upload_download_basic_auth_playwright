import pytest
import allure
from playwright.sync_api import sync_playwright, Page,expect
import time
import os

file_name = r"C:\AutomationTestingCourse\Playwright_projects2\tests\ex_04122024\upload_files\upload_sample.txt"
source_file = os.path.basename(file_name)
foldername = os.path.dirname(file_name)
print(source_file, foldername,sep="\t")
#time.sleep(10)
@pytest.fixture(scope="function")
def setup_teardown():
    """Fixture to initialize and teardown Playwright browser and page."""
    playwright = sync_playwright().start()  # Start Playwright
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # Load the login page
    page.goto("https://the-internet.herokuapp.com/")
    page.wait_for_load_state("networkidle")
    time.sleep(3)  # Reduce unnecessary sleep time
    yield page  # Provide the page object to tests

    # Teardown
    context.close()
    browser.close()
    playwright.stop()  # Ensure Playwright is properly stopped

@pytest.mark.positive
def test_file_upload(setup_teardown):
    """
    this is working with selected date
    :param setup_teardown:
    :return:
    """
    page = setup_teardown

    #file_upload link
    page.locator("//a[normalize-space()='File Upload']").click()
    time.sleep(3)
    expect(page).to_have_url("https://the-internet.herokuapp.com/upload")
    time.sleep(3)
    # Wait for the file chooser dialog to appear after clicking the upload button
    with page.expect_file_chooser() as file_chooser_info:
        page.locator("//input[@id='file-upload']").click()  # Simulate user clicking the file input
    file_chooser = file_chooser_info.value

    # Set the file to be uploaded
    file_chooser.set_files(file_name)  #
    # Additional interactions or verification
    time.sleep(3)
    page.locator("#file-submit").click()  # Submit if necessary
    time.sleep(3)
    upload_filename = page.locator("//div[@id='uploaded-files']").inner_text()
    #assert upload_filename == "upload_sample.txt", "The upload filename is not matching!"

    assert upload_filename == source_file, f"Expected file name '{source_file}', but got '{upload_filename}'"


@pytest.mark.positive
def test_file_download(setup_teardown):
    """
    this is working with selected date
    :param setup_teardown:
    :return:
    """
    page = setup_teardown

    #file_upload link
    page.locator("//a[normalize-space()='File Download']").click()
    time.sleep(3)
    expect(page).to_have_url("https://the-internet.herokuapp.com/download")
    time.sleep(3)

    with page.expect_download() as download_info:
        # Click the link using XPath
        page.locator("//a[@href='download/sample.pdf']").click()
    download = download_info.value

    # Save the downloaded file
    download_file = download.suggested_filename
    print("download_path:\n", download_file)
    #download_path = "tests/ex_04122024/upload_files"
    source = "C:\\Users\\Balraj\\Downloads\\"+download_file
    move_dest = foldername+"\\"+str(download_file)
    download.save_as(move_dest)

    # Assert the file was downloaded successfully
    assert f"download_path is {download_file}","path is different"
    print(f"Downloaded file: {download_file}")
