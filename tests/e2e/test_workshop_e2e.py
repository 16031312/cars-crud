import re

from playwright.sync_api import expect


def test_user_creates_car_in_browser(page, live_server):
    page.goto(f"{live_server}/cars/new")

    page.get_by_label("Make", exact=True).fill("Toyota")
    page.get_by_label("Model", exact=True).fill("Yaris")
    page.get_by_label("Year", exact=True).fill("2020")
    page.get_by_label("Color", exact=False).fill("Blue")
    page.get_by_role("button", name="Create car").click()

    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    expect(page.get_by_role("heading", name="Toyota Yaris")).to_be_visible()


def test_user_edits_car_and_change_survives_reload(page, live_server):
    page.goto(f"{live_server}/cars/new")

    page.get_by_label("Make", exact=True).fill("Honda")
    page.get_by_label("Model", exact=True).fill("Civic")
    page.get_by_label("Year", exact=True).fill("2022")
    page.get_by_label("Color", exact=False).fill("Blue")
    page.get_by_role("button", name="Create car").click()

    expect(page).to_have_url(re.compile(r"/cars/\d+$"))

    page.get_by_role("link", name="Edit car").click()

    model_input = page.get_by_label("Model", exact=True)
    model_input.click()
    model_input.fill("Accord")
    model_input.press("Tab")
    print("Model after fill:", model_input.input_value())

    year_input = page.get_by_label("Year", exact=True)
    year_input.click()
    year_input.fill("2023")
    year_input.press("Tab")
    print("Year after fill:", year_input.input_value())
    print("Model after year fill:", model_input.input_value())

    page.get_by_role("button", name="Save changes").click()

    expect(page).to_have_url(re.compile(r"/cars/\d+$"), timeout=15000)

    print("URL after save:", page.url)
    print("H1 texts:", page.locator("h1").all_text_contents())
    print("H2 texts:", page.locator("h2").all_text_contents())
    print("H3 texts:", page.locator("h3").all_text_contents())

    expect(page.get_by_role("heading", name="Honda Accord")).to_be_visible(timeout=15000)

    page.reload()
    expect(page.locator("#car-model")).to_have_text("Accord")
    expect(page.locator("#car-year")).to_have_text("2023")