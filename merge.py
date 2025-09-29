{\rtf1\ansi\ansicpg936\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # merge.py\
# \uc0\u29992 \u27861 \u65306 \u20250 \u35835 \u21462 \u29615 \u22659 \u21464 \u37327  UPSTREAM_URL, ANTI_AD_URL, OUTPUT_FILE, RULE_NAME\
# \uc0\u20063 \u21487 \u22312 \u26412 \u22320 \u27979 \u35797 \u26102 \u30452 \u25509 \u35774 \u32622 \u36825 \u20123 \u29615 \u22659 \u21464 \u37327 \u28982 \u21518 \u36816 \u34892 \u65306  python merge.py\
\
import os\
import sys\
import requests\
import yaml\
\
UPSTREAM_URL = os.getenv("UPSTREAM_URL")\
ANTI_AD_URL   = os.getenv("ANTI_AD_URL", "https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-clash.yaml")\
OUTPUT_FILE   = os.getenv("OUTPUT_FILE", "config.yaml")\
RULE_NAME     = os.getenv("RULE_NAME", "anti-ad")\
\
if not UPSTREAM_URL:\
    print("\uc0\u35831 \u35774 \u32622 \u29615 \u22659 \u21464 \u37327  UPSTREAM_URL (\u19978 \u28216  raw \u38142 \u25509 )\u12290 ")\
    sys.exit(2)\
\
print("fetching upstream:", UPSTREAM_URL)\
r = requests.get(UPSTREAM_URL, timeout=30)\
r.raise_for_status()\
upstream_text = r.text\
\
# \uc0\u35299 \u26512 \u19978 \u28216  yaml\u65288 \u23485 \u23481 \u22788 \u29702 \u65289 \
try:\
    upstream = yaml.safe_load(upstream_text) or \{\}\
except Exception as e:\
    print("\uc0\u35299 \u26512 \u19978 \u28216  YAML \u22833 \u36133 \u65306 ", e)\
    print("\uc0\u23558 \u19978 \u28216 \u20869 \u23481 \u20197 \u21407 \u26679 \u20445 \u23384 \u21040 ", OUTPUT_FILE)\
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:\
        f.write(upstream_text)\
    sys.exit(0)\
\
# \uc0\u30830 \u20445  rule-providers \u23383 \u27573 \u23384 \u22312 \u24182 \u21512 \u24182  anti-ad provider\
rp = upstream.get("rule-providers")\
if rp is None:\
    rp = \{\}\
else:\
    # \uc0\u20445 \u35777 \u26159  dict \u31867 \u22411 \
    if not isinstance(rp, dict):\
        rp = \{\}\
\
# \uc0\u22914 \u26524 \u24050 \u26377 \u21516 \u21517  provider\u65292 \u19981 \u35206 \u30422 \u65288 \u38500 \u38750 \u20320 \u24819 \u35206 \u30422 \u65289 \
if RULE_NAME in rp:\
    print(f"rule-providers \uc0\u20013 \u24050 \u26377  \{RULE_NAME\}\u65292 \u23558 \u19981 \u20250 \u35206 \u30422 \u12290 ")\
else:\
    rp[ RULE_NAME ] = \{\
        "type": "http",\
        "behavior": "domain",\
        "url": ANTI_AD_URL,\
        "interval": 86400\
    \}\
\
upstream["rule-providers"] = rp\
\
# \uc0\u30830 \u20445  rules \u23384 \u22312 \u24182 \u22312 \u26368 \u21069 \u38754 \u25554 \u20837  RULE-SET,NAME,REJECT\u65288 \u22914 \u26524 \u36824 \u27809 \u25554 \u20837 \u65289 \
rules = upstream.get("rules")\
if rules is None:\
    rules = []\
elif not isinstance(rules, list):\
    # \uc0\u26377 \u20123 \u25991 \u20214 \u25226  rules \u25918 \u25104 \u23383 \u31526 \u20018 \u25110 \u20854 \u20182 \u65292 \u19981 \u22826 \u24120 \u35265 \'97\'97\u23613 \u37327 \u23481 \u38169 \
    rules = list(rules)\
\
rule_line = f"RULE-SET,\{RULE_NAME\},REJECT"\
\
if rule_line not in rules:\
    # \uc0\u25554 \u20837 \u21040 \u26368 \u21069 \u38754 \u65288 \u20248 \u20808 \u32423 \u26368 \u39640 \u65289 \
    rules.insert(0, rule_line)\
    print("\uc0\u24050 \u22312  rules \u24320 \u22836 \u25554 \u20837 :", rule_line)\
else:\
    print("rules \uc0\u20013 \u24050 \u23384 \u22312 \u35813 \u34892 \u65292 \u19981 \u20877 \u37325 \u22797 \u25554 \u20837 \u12290 ")\
\
upstream["rules"] = rules\
\
# \uc0\u20889 \u22238  OUTPUT_FILE\
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:\
    yaml.safe_dump(upstream, f, sort_keys=False, allow_unicode=True)\
\
print("\uc0\u20889 \u20837 \u23436 \u25104  ->", OUTPUT_FILE)}