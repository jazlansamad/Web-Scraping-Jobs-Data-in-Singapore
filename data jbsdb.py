from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

headers = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/136.0.0.0 Safari/537.36')
}

base_url = 'https://sg.jobsdb.com/j?disallow=true&l=&q=data'
result = []

for p in range(1, 51):  # pages 1 to 50
    url = f"{base_url}&p={p}"
    print(f"Fetching page {p}: {url}")

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve page {p}")
        break

    soup = BeautifulSoup(response.text, 'html.parser')
    job_cards = soup.find_all('div', class_='job-card')

    if not job_cards:
        print(f"No more jobs found on page {p}")
        break

    for job in job_cards:
        title_tag = job.find('a', class_='job-link')
        company_tag = job.find('span', class_='job-company')
        location_tag = job.find('a', class_='job-location')
        salary_tag = job.find('div', class_='badge -default-badge')

        title = title_tag.text.strip() if title_tag else None
        company = company_tag.text.strip() if company_tag else None
        location = location_tag.text.strip() if location_tag else None
        salary = salary_tag.text.strip() if salary_tag else None

        result.append({
            'title': title,
            'company': company,
            'location': location,
            'salary': salary,
        })

    time.sleep(1)  # Be polite

# Save to CSV
df = pd.DataFrame(result)
df.to_csv("jobsdb_data_jobs.csv", index=False)
print("Saved to jobsdb_data_jobs.csv")