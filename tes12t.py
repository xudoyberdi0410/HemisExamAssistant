import requests

url = "https://student.fbtuit.uz/test/result/{id}"

payload = {}
headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'Accept-Language': 'en-GB,en;q=0.9,ru;q=0.8,en-US;q=0.7,zh-CN;q=0.6,zh;q=0.5',
  'Cache-Control': 'max-age=0',
  'Connection': 'keep-alive',
  'Cookie': 'frontend=f53s3vrdspkiutjc9rtpmuhd8k; _csrf-frontend=04f2989d18876bfee2e2d9ea10d188108b8cfba0d62cbb4b7d6ee9bfd686b3b0a%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%22iBdvB4IJgLN5VcDSm1eT7L6bPPHuFPtt%22%3B%7D; _csrf-frontend=7982ef3435fe89816fc1babd50d26de902437d3e5947b9ae79ceac1008ae9cd7a%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%22lQ7gIdaxuMfasCIcj9qcGEjqPDCBD-Ld%22%3B%7D; frontend=un01astprkbv0ujq0l9ck6cfaj',
  'Referer': 'https://student.fbtuit.uz/education/tasks?subject=20',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-User': '?1',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}

response = requests.request("GET", url.format(id=507893), headers=headers, data=payload, allow_redirects=False)

print(response.status_code)
