import requests, re, time
import xml.etree.ElementTree as ET

SITEMAP = "https://www.icici.bank.in/sitemap-index.xml"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

def get_urls(sm):
    try:
        r = requests.get(sm, headers=HEADERS, timeout=30)
        if r.status_code != 200: return []
        root = ET.fromstring(r.content)
        ns = ""
        m = re.match(r'\{.*\}', root.tag)
        if m: ns = m.group(0)
        locs = [elem.text for elem in root.findall(f".//{ns}loc")]
        if not locs: locs = re.findall(r"<loc>(.*?)</loc>", r.text)
        out = []
        for l in locs:
            l = l.strip()
            if l.endswith(".xml"): out += get_urls(l)
            else: out.append(l)
        return out
    except Exception:
        return []

def save_to_wayback(url):
    api_url = f"https://web.archive.org/save/{url}"
    try:
        response = requests.post(api_url, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            print(f"Successfully requested Wayback archival for: {url}")
        else:
            print(f"Failed {url}: HTTP {response.status_code}")
    except Exception as e:
         print(f"Error {url}: {e}")

def main():
    urls = get_urls(SITEMAP)
    if not urls:
        print("No URLs found.")
        return
    
    print(f"Found {len(urls)} URLs. Archiving...")
    # Currently set to the first 10 URLs. You can remove `[:10]` to archive everything.
    for u in urls[:10]:
        save_to_wayback(u)
        time.sleep(5)  # Required sleep interval to respect Wayback API limits

if __name__ == '__main__':
    main()
