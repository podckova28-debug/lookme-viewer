# Legal, regulatory and tax framework for individuals earning from affiliate links, referral programs and online advertising in Russia (state as of September 2026)

Method note for the report writer: every page fetch (WebFetch) was blocked by the network egress proxy for all Russian domains, including consultant.ru, garant.ru, nalog.gov.ru and pravo.gov.ru. The session's shared web-search budget (200 calls) ran out partway through this task. As a result, all cited findings below come from search-engine result summaries of the linked pages, not from full-text reads. Figures and dates were cross-checked across several results where possible, and conflicts are flagged. Topics I could not verify (bank referral bonus taxation, cashback, deposit-interest threshold, financial-services advertising rules, progressive НДФЛ, VPN/crypto ad bans, pending 2026 bills) are in the Gaps sections. Where I wrote down background knowledge there, it is labelled as unverified.

## 1. Маркировка интернет-рекламы (ФЗ-347, ст. 18.1 Закона «О рекламе» 38-ФЗ): when affiliate content is advertising, ERID, ОРД, ЕРИР, responsibility, fines, CPA-network practice

### Takeaway
Since 1 Sept 2022, every piece of internet advertising, including affiliate/referral links and blogger posts, must carry the label «Реклама», an erid token issued by an ОРД, and advertiser details, and must be reported via an ОРД to ЕРИР (Roskomnadzor's register). CPA networks such as Admitad register the creatives and put the erid into the partner link. The webmaster must keep the marking visible and make sure statistics are reported. Fines are 2,000–2,500 ₽ for citizens for unmarked ads (ч.1 ст.14.3 КоАП) and 10,000–30,000 ₽ for citizens for ЕРИР reporting failures (ч.15 ст.14.3), rising to 200,000–500,000 ₽ for legal entities. Since September 2025, reporting obligations have been time-limited (about 1 year) instead of "perpetual".

### Cited Findings
- **Scope and required elements.** Since 1 Sept 2022 all internet advertising must be marked, including blogger reviews, giveaways and banners. The marking must contain the word «Реклама», a unique ID token (erid) and advertiser information (name and ИНН). — [РИА Новости](https://ria.ru/20250316/markirovka-1896148209.html); [ГАРАНТ.РУ](https://www.garant.ru/consult/popularnie-voprosi/2010539/); [Callibri](https://callibri.ru/blog/markirovka-reklamy-novye-pravila-izmeneniya)
- **What erid is.** The erid is a unique alphanumeric identifier that the operator of advertising data (ОРД) assigns to each advertising creative. It confirms that the ad is registered. — [Альфа-Курс](https://kurs.alfabank.ru/articles/ord-erir-erid-chto-vsyo-ehto-znachit-i-kak-markirovat-reklamu/); [Admitad blog](https://www.admitad.ru/blog/advertising-marking/)
- **What ЕРИР is.** ЕРИР (Единый реестр интернет-рекламы) is run under Roskomnadzor. Data on contracts, acts, creatives and impression statistics reach it through ОРД. — [syce.ru](https://syce.ru/blog/markirovka-reklamy-2026); [chimitdorzhi.tech](https://chimitdorzhi.tech/blog/markirovka-reklamy-ord-2026/)
- **Affiliate links are advertising.** CPA-network guides state that any affiliate/partner link requires marking. The parameter `erid=xxxx` is appended to the click link, or the erid is placed at the start of the post. — [e-Контур](https://e-kontur.ru/blog/16008/erid-v-ssylke); [Где Слон?](https://gdeslon.ru/faq/115/); [ePN](https://epn.bz/ru/info/ads-marking-guide/); [САЛИД](https://salid.ru/journal/zakon-o-markirovke-reklamy-kak-partnyoram-salid-markirovat-reklamu)
- **How Admitad handles marking.**
  - Admitad sends all creatives in its network to an ОРД and registers them in ЕРИР. It inserts a unique token for each creative into the affiliate link.
  - It marks banners «Реклама» and passes creative statistics to the ОРД at the end of each month.
  - The erid must be visible to users and copyable. If affiliate links are hidden behind intermediate pages, extra marking information beyond the erid in the link is needed.
  - Source: [Admitad support FAQ](https://support.admitad.ru/knowledge-base/article/faq-%D0%BF%D0%BE-%D0%BC%D0%B0%D1%80%D0%BA%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B5-%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D1%8B-%D0%B4%D0%BB%D1%8F-%D0%B2%D0%B5%D0%B1-%D0%BC%D0%B0%D1%81%D1%82%D0%B5%D1%80%D0%BE%D0%B2_1); [Admitad blog](https://www.admitad.ru/blog/advertising-marking/)
- **Webmaster's side in CPA networks.** Webmasters can get pre-marked creatives in their CPA dashboard. Reports with "разаллокация" of acts and impression statistics go to the ОРД within 30 days after the end of the reporting month. Whoever registered the creatives does the разаллокация. — [cpa.hh.ru на vc.ru](https://vc.ru/headhunter/823678-markirovka-reklamy-i-shemy-raboty-s-ord-ultimativnyi-spravochnik-ot-komandy-cpahhru); [Где Слон?](https://gdeslon.ru/faq/115/)
- **Put the split in writing.** Partners should record in the contract or correspondence who obtains the erid and who reports to the ОРД. — [prmonline](https://prmonline.ru/blog/markirovka-reklamy-v-partnerskom-marketinge-chto-eto-i-zachem); [Admitad support](https://support.admitad.ru/knowledge-base/article/faq-%D0%BF%D0%BE-%D0%BC%D0%B0%D1%80%D0%BA%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B5-%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D1%8B-%D0%B4%D0%BB%D1%8F-%D0%B2%D0%B5%D0%B1-%D0%BC%D0%B0%D1%81%D1%82%D0%B5%D1%80%D0%BE%D0%B2_1)
- **Statistics deadline.** Data on actual impressions and platforms must reach ЕРИР within 30 calendar days after the end of the month of placement. Missing this is the most common ground for fines under ч.15 ст.14.3 КоАП. — [chimitdorzhi.tech](https://chimitdorzhi.tech/blog/markirovka-reklamy-ord-2026/); [Ветров и партнёры](https://vitvet.com/articles/koap/otrasli/reklama-v-internete-narusheniya-shtraf-2026/)
- **Fine, ч.1 ст.14.3 КоАП** (general breach of the advertising law, including unmarked ads, by the advertiser, producer or distributor):

  | Who | Fine |
  |---|---|
  | Citizens (граждане) | 2,000–2,500 ₽ |
  | Officials (должностные лица) | 4,000–20,000 ₽ |
  | Legal entities (юрлица) | 100,000–500,000 ₽ |

  Sources: [КонсультантПлюс, ст.14.3 КоАП](https://www.consultant.ru/document/cons_doc_LAW_34661/2d50fc1c4013ea9ab20b8b2666c1650b1dc4c982/); [Ветров и партнёры](https://vitvet.com/articles/koap/sostavy/shtraf-narushenie-zakona-reklame-14-3-2026/)
- **Fine, ч.15 ст.14.3 КоАП** (failure to submit data to ЕРИР, late submission, or incomplete/false/outdated data):

  | Who | Fine |
  |---|---|
  | Citizens | 10,000–30,000 ₽ |
  | Officials | 30,000–100,000 ₽ |
  | Legal entities | 200,000–500,000 ₽ |

  Sources: [Ветров и партнёры](https://vitvet.com/articles/koap/otrasli/reklama-v-internete-narusheniya-shtraf-2026/); [syce.ru](https://syce.ru/blog/markirovka-reklamy-2026); [Клерк](https://www.klerk.ru/blogs/klerk_business/671150/)
- **Fine per placement, by status (as the search summaries give it):**

  | Status | Fine per violating post |
  |---|---|
  | Individuals | up to 2,500 ₽ |
  | ИП and officials | up to 20,000 ₽ |
  | Small businesses | up to 250,000 ₽ |
  | Medium and large businesses | up to 500,000 ₽ |

  Sources: [Promopult](https://blog.promopult.ru/law/registraciya-v-rkn-i-shtrafy-dlya-blogerov-desyatitysyachnikov.html); [eLama](https://elama.ru/blog/registraciya-blogerov-v-roskomnadzore-gayd-po-novomu-zakonu/)
- **Conflicting claim.** Some popular explainers say fines run "from 30,000 to 500,000 ₽ per post without erid" and "30,000–100,000 ₽ for self-employed". This does not match the citizen bands in ч.1/ч.15 ст.14.3 above. The 30–100k figure is the *officials* band of ч.15. — claim in [eLama](https://elama.ru/blog/oshtrafah-iotvetstvennosti-zanesoblyudenie-zakona-omarkirovke-reklamy/) / [finbazar](https://finbazar.ru/post/609040-shtrafy-dlya-blogerov-2026); contradicted by [КонсультантПлюс](https://www.consultant.ru/document/cons_doc_LAW_34661/2d50fc1c4013ea9ab20b8b2666c1650b1dc4c982/) and [Ветров и партнёры](https://vitvet.com/articles/koap/otrasli/reklama-v-internete-narusheniya-shtraf-2026/)
- **Both sides can be fined.** Delegating marking to an agent does not remove the advertiser's liability. If the agent or blogger fails to mark, both can be fined. — [Ветров и партнёры](https://vitvet.com/articles/koap/sostavy/shtraf-narushenie-zakona-reklame-14-3-2026/); [eLama](https://elama.ru/blog/oshtrafah-iotvetstvennosti-zanesoblyudenie-zakona-omarkirovke-reklamy/)
- **Enforcement is rising.**
  - Jan–May 2025: 230 fine decisions for marking violations, against 96 in the same period of 2024. — [eLama](https://elama.ru/blog/oshtrafah-iotvetstvennosti-zanesoblyudenie-zakona-omarkirovke-reklamy/); [РИА Новости](https://ria.ru/20250316/markirovka-1896148209.html) (same result set)
  - ФАС sharply increased internet-ad checks in 2024–2025. Internet ads account for more than 40% of all advertising-law violations it found. — [Ветров и партнёры](https://vitvet.com/articles/koap/sostavy/shtraf-narushenie-zakona-reklame-14-3-2026/)
- **Change from September 2025: reporting period limited (supersedes "perpetual reporting").**
  - Government decree (Постановление Правительства) № 1427, reported as in force from 18 Sept 2025. Advertisers can stop reporting ads placed more than a year ago.
  - The ЕРИР storage period drops from 5 to 3 years. Reported effective date: "from 1 September".
  - Ads in Instagram published before 1 Sept 2025 must be reported for 1 year from publication.
  - The sources say an exception keeps perpetual reporting for ads embedded in authors' videos on YouTube, Rutube and similar platforms.
  - Sources: [Кабельщик](https://www.cableman.ru/content/srok-otchetnosti-po-reklame-ogranichen-odnim-godom); [Эксперт](https://expert.ru/news/assotsiatsiya-blogerov-i-agentstv-dobilas-otmeny-vechnoy-otchetnosti-po-reklame/); [Клерк](https://www.klerk.ru/user/2416162/663028/); [Callibri](https://callibri.ru/blog/novye-pravila-otchetnosti-za-reklamu)
  - Another explainer puts it as "until 1 Sept 2025 the obligation was perpetual, now it is limited to one year". — [Callibri](https://callibri.ru/blog/markirovka-reklamy-novye-pravila-izmeneniya)
  - The exact effective date (1 Sept vs 18 Sept 2025) differs between sources.
- **Date discrepancy on liability.** One source says that "from 1 Sept 2023" all internet ads must carry «Реклама», a token and advertiser details. This conflicts with the 1 Sept 2022 date of the law. See Inferences. — [Ветров и партнёры](https://vitvet.com/articles/koap/sostavy/shtraf-narushenie-zakona-reklame-14-3-2026/)

### Inferences
- For an individual affiliate who posts marketplace or bank links through a CPA network (Admitad, Где Слон?, САЛИД, ePN and similar), the network typically registers creatives and issues the erid. The individual still has to:
  1. use the erid-tagged link or creative as-is;
  2. add «Реклама» and the advertiser's name/ИНН, or a link to them, in the post;
  3. make sure impression statistics for their placements reach the ОРД within 30 days after month end, either through the network or themselves if they self-register.
  Posting a "raw" referral link without an erid is the core exposure.
- An ИП is fined in the "officials" band (4–20k under ч.1; 30–100k under ч.15). This matches the "ИП and officials up to 20,000" wording above. A plain individual or a самозанятый is fined as a citizen.
- The 2022 vs 2023 discrepancy most likely reflects a transition period: the law applied from 1 Sept 2022, but fines were actively imposed from 1 Sept 2023. I could not verify this in this session.

### Gaps
- Could not read the text of 38-ФЗ ст.18.1 or the ФАС/Roskomnadzor positions on when a self-referral or "non-commissioned" product link or promo code is (or is not) advertising, for example a personal recommendation vs a paid link. Background (unverified): ФАС treats information that picks out a specific product and aims to promote it, especially for payment or commission, as advertising.
- Could not verify the current list of accredited ОРД or their fees for self-registration (e.g., Яндекс ОРД, VK ОРД, ОЗОН ОРД, Медиаскаут, Первый ОФД, ОРД-А/Amberdata) as of 2026.
- Could not confirm the exact КоАП part numbers, or whether any 2025–2026 amendments changed the fine bands. A background claim that ЕРИР fines sit in "ст.14.64" appears wrong: search results show ст.14.64 concerns construction СРО. Verify on consultant.ru.
- Could not confirm whether marking and reporting by marketplaces' in-house affiliate programs (Ozon Blogger, WB, Яндекс Маркет) is done by the platform or by the blogger.

## 2. Обязательный сбор 3% с интернет-рекламы (ст.18.2 38-ФЗ, from 1 April 2025): who pays, bloggers and affiliates, 2026 changes

### Takeaway
Since 1 April 2025, distributors of internet advertising aimed at Russian consumers pay 3% of quarterly advertising income to the federal budget. Payers include bloggers, site owners, ad systems and agents/intermediaries. Roskomnadzor administers the fee from ЕРИР data. An agent may pay for the whole chain, which in practice often relieves bloggers and webmasters paid through agencies or CPA networks. Rules were set by decree № 1224 (15.08.2025) and had not materially changed as of 2026, apart from calendar shifts in payment dates.

### Cited Findings
- **Legal basis and start date.** Federal Law № 479-ФЗ of 26.12.2024 added art. 18.2 «Обязательные отчисления за распространение рекламы в сети Интернет» to the Law on Advertising. It applies to advertising distributed from Q2 2025 (from 1 April 2025). The first payment was due in Q3 2025. — [Lidings](https://www.lidings.com/ru/media/legalupdates/compulsory_deductions/); [КонсультантПлюс, ст.18.2](https://www.consultant.ru/document/cons_doc_LAW_58968/f5499f6a99f4f1011e473eae3412f6c7f0262387/)
- **Payment rules.** Calculation and payment rules were approved by Government decree № 1224 of 15.08.2025. — [КонсультантПлюс](https://www.consultant.ru/legalnews/29272/); [Альфа-Курс](https://kurs.alfabank.ru/articles/reklamnyj-sbor-poryadok-raschyota-i-uplaty-po-itogam-kvartala/)
- **Who pays.** Payers are companies and individuals with income from placing internet advertising aimed at a Russian audience. This covers рекламораспространители (bloggers, site owners, media), operators of advertising systems (e.g., Яндекс Директ, VK Реклама), and intermediaries/agents acting for advertisers. — [Lidings](https://www.lidings.com/ru/media/legalupdates/compulsory_deductions/); [eLama](https://elama.ru/blog/faq-po-sboru-3-za-dohod-ot-reklamy-otvechayut-eksperty-elama/)
- **Self-employed and ИП are in scope.** T-Bank's explainer states that all participants in the chain, including самозанятые and ИП, pay from 1 April 2025. — [Т-Банк Бизнес-секреты](https://secrets.tbank.ru/buhgalteriya/novyj-sbor-za-internet-reklamy/)
- **The agent can pay for the chain.** An agent can pay the fee for all participants in the chain and so release them from the obligation. — [dhprime](https://dhprime.ru/blog/reklamnyy-sbor/reklamnyy-sbor-3-chem-grozyat-rynku-internet-reklamy-opublikovannye-npa-ot-roskomnadzora/); [ЭдПрав](https://edlegal.ru/blog/reklamnyj-sbor-3-procenta-2025/); [wowblogger](https://wowblogger.ru/blog/sbor_3_ot_dohodov_s_internet_reklamy)
- **Advertisers ordering through an agency do not pay.** If an advertiser simply orders blogger ads through a Russian agency, the agency or blogger pays, not the advertiser. — [eLama](https://elama.ru/blog/faq-po-sboru-3-za-dohod-ot-reklamy-otvechayut-eksperty-elama/)
- **Exemptions.** Sites of TV and radio channels and news agencies are exempt, as are network media with state or municipal participation or budget funding. — [eLama](https://elama.ru/blog/faq-po-sboru-3-za-dohod-ot-reklamy-otvechayut-eksperty-elama/); [Lidings](https://www.lidings.com/ru/media/legalupdates/compulsory_deductions/)
- **Worked example.** A blogger who earned 500,000 ₽ from placements owes 15,000 ₽ (3%). — [eLama](https://elama.ru/blog/novyy-nalog-na-reklamu-v-2025-godu-v-rossii-vvedut-obyazatelnye-otchisleniya-s-dohoda-ot-promo-v-internete/)
- **Procedure.** Roskomnadzor publishes the calculation in the payer's personal account by the 15th of the second month after the quarter. Payment is due by the 5th of the third month after the quarter. — [eLama](https://elama.ru/blog/faq-po-sboru-3-za-dohod-ot-reklamy-otvechayut-eksperty-elama/); [Альфа-Курс](https://kurs.alfabank.ru/articles/reklamnyj-sbor-poryadok-raschyota-i-uplaty-po-itogam-kvartala/)
- **2026 payment calendar.** Two dates shift because the 5th falls on a weekend. — [Law.ru](https://www.law.ru/news/43713-v-2026-godu-srok-uplaty-reklamnogo-sbora-sdvinetsya-dvajdy); [Альфа-Курс](https://kurs.alfabank.ru/articles/reklamnyj-sbor-poryadok-raschyota-i-uplaty-po-itogam-kvartala/)

  | Quarter | Payment due |
  |---|---|
  | Q4 2025 | 5 March 2026 |
  | Q1 2026 | 5 June 2026 |
  | Q2 2026 | 7 September 2026 |
  | Q3 2026 | 7 December 2026 |

- **Revenue.** Nearly 8 billion ₽ reached the budget in the first six months. Proceeds support the IT industry and are supervised by Roskomnadzor using automated ЕРИР data. — [Sostav](https://www.sostav.ru/blogs/239662/67464); [Т-Банк](https://secrets.tbank.ru/buhgalteriya/novyj-sbor-za-internet-reklamy/)
- **Collection of arrears.** If Roskomnadzor finds non-payment or underpayment, it sends a notice. If the fee is not paid within 10 calendar days, it recovers it through the courts. — [Клерк](https://www.klerk.ru/blogs/klerk_business/671150/); [1С:ИТС](https://its.1c.ru/db/content/bizlegsup/src/4050304_%D1%82_%D0%BC%D0%BE%D0%BD%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%BD%D0%B3_%D1%83%D0%BF%D0%BB%D0%B0%D1%82%D1%8B.htm)
- **Fines for non-payment (sources disagree).**
  - One source cites ч.1 ст.14.3 КоАП: companies 100,000–500,000 ₽, officials 4,000–20,000 ₽. — [Клерк](https://www.klerk.ru/blogs/klerk_business/671150/)
  - Another gives up to 2,500 ₽ for individuals, up to 20,000 ₽ for ИП and up to 500,000 ₽ for legal entities. — [eLama](https://elama.ru/blog/faq-po-sboru-3-za-dohod-ot-reklamy-otvechayut-eksperty-elama/)
  - Roskomnadzor called the main risk a fine of up to 500,000 ₽ for false information, i.e. the ЕРИР data behind the calculation. — [26-2.ru](https://e.26-2.ru/1173161)
- **No change to the fee found for 2026.** By 2026 the rules had "stabilized". — [Sostav](https://www.sostav.ru/blogs/239662/67464)
  - A separate March 2026 initiative for a 3% levy on marketplaces/delivery operators in favour of «Почта России» was left out of the Минцифры draft law. That is not a change to the advertising fee. — [ComNews, 26.03.2026](https://www.comnews.ru/content/244419/2026-03-26/2026-w13/1008/mincifry-ne-vklyuchilo-zakonoproekt-normu-o-3-nom-sbore-marketpleysov-polzu-pochty-rossii)

### Inferences
- An affiliate paid by a CPA network or agency is formally a рекламораспространитель in the chain. However, the network/agent is allowed to pay for the whole chain. So in practice the individual webmaster usually does not pay the 3% separately, provided the network declares that it pays for the chain. This should be confirmed in the network's offer or contract.
- A blogger who contracts directly with an advertiser (e.g., a direct deal with a bank or brand) is most exposed to paying the fee personally, through the Roskomnadzor personal account.
- The fee is calculated from ЕРИР data. Marking and reporting discipline and the fee are therefore linked: wrong ЕРИР data means a wrong fee calculation, plus a ч.15 ст.14.3 fine.

### Gaps
- Could not read decree № 1224 to confirm the exact wording of the "agent pays for the chain" mechanism. I also could not confirm whether revenue already subject to the fee upstream is excluded downstream.
- Could not confirm whether the fee applies to CPA/CPS affiliate commissions from marketplace in-house programs (Ozon Blogger, WB, Яндекс Маркет), where the marketplace is both advertiser and program operator.
- Did not find any enacted 2026 amendment to art. 18.2 (rate, thresholds, small-blogger exemption). If such bills exist, they were not surfaced.

## 3. Bans on advertising on certain resources: иноагенты (2024), banned/extremist and blocked resources incl. Instagram (1 Sept 2025), Telegram and other pages with 10,000+ subscribers (303-ФЗ)

### Takeaway
There are three platform-level bans that an affiliate must check before posting any paid or affiliate content:
1. No ads on resources of foreign agents, and no ads of foreign agents (42-ФЗ, in force 22.03.2024).
2. No ads on resources of undesirable, extremist or terrorist organizations, or on any resource blocked in Russia (72-ФЗ, from 01.09.2025). This covers Instagram and Facebook, including blogger posts.
3. No ads, reposts or donation calls on personal pages with more than 10,000 subscribers that are not in Roskomnadzor's list (303-ФЗ: data submission from 01.11.2024, ad ban from 01.01.2025).

Violations are generally fined under ст.14.3 КоАП against both advertiser and distributor, per placement.

### Cited Findings
- **Foreign agents (иноагенты), 42-ФЗ.**
  - Federal Law of 11.03.2024 № 42-ФЗ bans advertising on information resources of foreign agents and advertising of foreign agents. It amended the laws on advertising, on mass media, and on control over persons under foreign influence. It entered into force on 22 March 2024. — [ЭЛКОД](https://elcode.ru/service/news/obzory-zakonodatelstva-dlya-sudey/s-22-marta-2024-goda-vstupil-v-silu-zakon-o-zapret); [ГАРАНТ.РУ](https://www.garant.ru/news/1689005/); [Ведомости](https://www.vedomosti.ru/politics/news/2024/03/11/1024616-putin-podpisal)
  - "Resources" means any source: websites, VK groups, blogs, Telegram and YouTube channels, on Russian or foreign platforms. — [Коммерсантъ](https://www.kommersant.ru/doc/6552366); [АСИ](https://asi.org.ru/2024/03/19/zapret-na-reklamu/)
  - Fines reported inconsistently:
    - Citizens up to 50,000 ₽ and organizations up to 500,000 ₽. — [Коммерсантъ](https://www.kommersant.ru/doc/6552366)
    - Citizens up to 50,000 ₽ and legal entities up to 300,000 ₽ under ч.42 ст.19.5 КоАП. — [ЭЛКОД](https://elcode.ru/service/news/obzory-zakonodatelstva-dlya-sudey/s-22-marta-2024-goda-vstupil-v-silu-zakon-o-zapret)
    - Media can get a warning, then a fine of up to 300,000 ₽. — [Коммерсантъ](https://www.kommersant.ru/doc/6552366)
    - Both advertiser and distributor are liable. — [ЭЛКОД](https://elcode.ru/service/news/obzory-zakonodatelstva-dlya-sudey/s-22-marta-2024-goda-vstupil-v-silu-zakon-o-zapret)
- **Banned, extremist and blocked resources, 72-ФЗ.**
  - Federal Law of 07.04.2025 № 72-ФЗ amended art. 12 of the Law on Countering Extremist Activity and the Law on Advertising. From 1 Sept 2025 it bans advertising on:
    - information resources of undesirable foreign/international organizations;
    - resources of organizations liquidated or banned by court for extremism or terrorism;
    - other information resources to which access is restricted under Russian IT law, i.e. blocked sites and platforms.
  - Sources: [ГАРАНТ.РУ](https://www.garant.ru/hotlaw/federal/1807775/); [Kremlin.ru](http://www.kremlin.ru/acts/bank/51808); [pravo.gov.ru](http://publication.pravo.gov.ru/document/0001202504070018); [Б1](https://b1.ru/insights/law-messenger/advertising-on-prohibited-resources-8-april-2025/); [РБК](https://www.rbc.ru/rbcfreenews/67e288e29a7947c0d74be792)
  - Instagram and Facebook (Meta is recognised as extremist) fall under the ban. Targeted ads there were already banned. From 1 Sept 2025 the ban also covers ads by bloggers and in public accounts, including posts and stories that prompt purchase. — [eLama](https://elama.ru/blog/zapret-reklamy-v-instagram-s-1-sentyabrya-2025-chto-izmenitsya-i-kak-rabotat-po-novomu-zakonu/); [Forbes.ru](https://www.forbes.ru/svoi-biznes/544859-zapret-reklamy-v-instagram-s-1-sentabra-cto-mozno-i-nel-za-publikovat); [ГАРАНТ.РУ](https://www.garant.ru/article/1845542/)
  - Fines go up to 500,000 ₽. Both the advertiser and the account owner can be fined, separately for each placement: one story plus one post can mean two fines. — [ADPASS](https://adpass.ru/zapret-reklamy-v-instagram-i-facebook-s-1-sentyabrya-2025-goda-chto-budet-so-starymi-postami-i-kakie-shtrafy-grozyat-biznesu/); [Jivo](https://www.jivo.ru/blog/ecommerce/zapret-reklamy-v-instagram-kak-biznesu-izbezhat-shtrafov-v-novykh-usloviyakh.html)
  - Influencers face up to 20,000 ₽ and companies up to 500,000 ₽. — [Точка](https://allo.tochka.com/zapret-reklamy-v-inst)
  - Old ads published before 1 Sept 2025 are not covered if they are not distributed or referenced after that date. Ads placed after 1 Sept 2025 can be fined up to a year later. — [eLama](https://elama.ru/blog/zapret-reklamy-v-instagram-s-1-sentyabrya-2025-chto-izmenitsya-i-kak-rabotat-po-novomu-zakonu/); [ADPASS](https://adpass.ru/zapret-reklamy-v-instagram-i-facebook-s-1-sentyabrya-2025-goda-chto-budet-so-starymi-postami-i-kakie-shtrafy-grozyat-biznesu/)
- **Personal pages with more than 10,000 subscribers, 303-ФЗ.**
  - Under Federal Law of 08.08.2024 № 303-ФЗ, owners and administrators of personal pages or channels with more than 10,000 subscribers must, from 1 Nov 2024, submit identifying data to Roskomnadzor. — [Т-Банк](https://secrets.tbank.ru/trendy/registraciya-v-reestre-rkn/); [ОУЗС](https://ouzs.ru/news/analiticheskaya-spravka-po-federalnomu-zakonu-ot-08-08-2024-303-fz-/); [КонсультантПлюс](https://www.consultant.ru/legalnews/27463/)
  - From 1 Jan 2025, for pages not in the list:
    - advertisers cannot place ads there;
    - reposts of their messages are restricted;
    - calls for financing (donations, paid subscriptions) are prohibited.
  - Sources: [GetCourse](https://getcourse.ru/marketing-blog/1146797/chto-budet-esli-ne-vpisat-svoe-imya-v-reestr-roskomnadzora); [Т-Банк](https://secrets.tbank.ru/trendy/registraciya-v-reestre-rkn/); [Yandex для бизнеса](https://b2b.yandex.ru/adv/edu/materials/registraciya-blogerov-ot-10000-podpischikov)
  - Registration is through Госуслуги or the Roskomnadzor website. Roskomnadzor checks the data within 7 working days. — [ГАРАНТ.РУ](https://www.garant.ru/news/1764927/); [Т-Банк](https://secrets.tbank.ru/trendy/registraciya-v-reestre-rkn/)
  - Advertisers must check that a blog with more than 10,000 subscribers is in the list before buying ads. Both blogger and advertiser are fined under ст.14.3 КоАП for ads in unregistered blogs. Fines per publication: individuals up to 2,500 ₽; ИП and officials up to 20,000 ₽; small business up to 250,000 ₽; medium and large business up to 500,000 ₽. — [Promopult](https://blog.promopult.ru/law/registraciya-v-rkn-i-shtrafy-dlya-blogerov-desyatitysyachnikov.html); [eLama](https://elama.ru/blog/registraciya-blogerov-v-roskomnadzore-gayd-po-novomu-zakonu/); [СберБизнес](https://sberbusiness.live/publications/registraciya-blogerov-v-reestre-rkn)

### Inferences
- An affiliate whose Telegram channel, VK group or other page passes 10,000 subscribers must register before running any affiliate or ad posts. Otherwise every such post is an unlawful placement, and CPA networks and advertisers will usually refuse to work with the channel.
- Instagram, Facebook and any other resource blocked in Russia cannot be used for affiliate links to Russian marketplaces or banks at all since 1 Sept 2025. Traffic must move to VK, MAX, Telegram (registered if over 10k), Дзен, Rutube, own sites and similar.
- Before placing ads on third-party channels, for example when buying traffic, check that the channel is not a foreign agent's resource. Such an ad exposes the advertiser/affiliate too.

### Gaps
- Could not confirm the precise КоАП parts and amounts applied to the иноагент ban. Sources conflict (ч.1 ст.14.3 vs ч.42 ст.19.5; 300k vs 500k for legal entities).
- Could not verify whether any 2025–2026 amendment added separate КоАП fines specifically for failing to register a 10k+ page. Background (unverified): there were proposals to fine page owners for not submitting data.
- Could not verify whether ads *for* VPN services are banned. Background (unverified): 406-ФЗ of 31.07.2023, from 1 March 2024, bans advertising of means of bypassing blocking. This is relevant to affiliates, since VPN offers are common in CPA networks.

## 4. Taxation: НПД, ИП on УСН (incl. 2026 НДС thresholds), НДФЛ; statuses accepted by CPA and in-house programs; taxability of referral bonuses and cashback

### Takeaway
The cheapest legal route for an individual affiliate in 2026 is НПД (самозанятый):
- 4% on income from individuals, 6% on income from legal entities and ИП;
- a one-off 10,000 ₽ deduction lowers effective rates to 3%/4% until used up;
- income limit 2.4 million ₽ a year;
- the regime is guaranteed until 2028.

Above that limit, ИП on УСН «доходы» at 6% is the usual choice. It carries fixed contributions of 57,390 ₽ in 2026 plus 1% of income over 300,000 ₽. From 2026 it also has a much lower НДС-exemption threshold: 20 mln ₽ in 2026, 15 mln ₽ in 2027, 10 mln ₽ from 2028. The 60 mln ₽ threshold of 2025 is superseded.

Marketplace in-house programs (Ozon Blogger, WB, Яндекс Маркет) mostly require самозанятый, ИП or company status.

### Cited Findings
- **НПД rates for 2026.** Unchanged: 4% on income from individuals, 6% on income from legal entities and ИП. — [Главбух](https://www.glavbukh.ru/art/390747-samozanyatye-v-2026-godu-izmeneniya-stavki-nalogi-kak-pereyti-s-1-yanvarya); [Контур](https://kontur.ru/articles/4818)
- **НПД limit.** Income limit stays at 2.4 million ₽ a year. Exceeding it means losing НПД status and falling back to ordinary individual taxation (НДФЛ). — [Главбух](https://www.glavbukh.ru/art/390747-samozanyatye-v-2026-godu-izmeneniya-stavki-nalogi-kak-pereyti-s-1-yanvarya); [RB.ru](https://rb.ru/reviews/samozanyatost-2026/)
- **НПД deduction.** The 10,000 ₽ tax deduction still applies. While it lasts, the 4% rate becomes 3% and the 6% rate becomes 4%. — [Главбух](https://www.glavbukh.ru/art/390747-samozanyatye-v-2026-godu-izmeneniya-stavki-nalogi-kak-pereyti-s-1-yanvarya)
- **НПД future.** Abolishing НПД in 2026 was discussed, but the regime stays until 2028. Proposals for a single 5% rate or progression above 2.4 million ₽ were postponed to 2028. — [e-Контур](https://e-kontur.ru/enquiry/2657/otmenyat-li-npd); [Главбух](https://www.glavbukh.ru/art/390747-samozanyatye-v-2026-godu-izmeneniya-stavki-nalogi-kak-pereyti-s-1-yanvarya)
- **УСН НДС thresholds (supersede 60 mln ₽ in 2025).** Under Federal Law № 425-ФЗ of 28.11.2025, the income threshold for НДС exemption on УСН is 20 mln ₽ in 2026, 15 mln ₽ in 2027 and 10 mln ₽ from 2028. The thresholds are not indexed. — [Контур.Экстерн](https://www.kontur-extern.ru/info/81877-usn_i_nds); [ГАРАНТ.РУ](https://www.garant.ru/consult/popularnie-voprosi/2040005/); [Клерк](https://www.klerk.ru/user/2709974/704372/)
  - Above the threshold, a УСН payer must charge and pay НДС, keep purchase and sales books, and file НДС returns. — [Контур.Экстерн](https://www.kontur-extern.ru/info/81373-nalogovaya_reforma_izmeneniya_po_specrezhimam)
- **ИП insurance contributions for 2026.**
  - Fixed part: 57,390 ₽, due by 28 Dec 2026.
  - Additional part: 1% of income above 300,000 ₽, capped at 321,818 ₽ for 2026, due by 1 July 2027.
  - Sources: [Regberry](https://www.regberry.ru/nalogooblozhenie/fiksirovannye-vznosy-ip-2026); [e-Контур](https://e-kontur.ru/enquiry/29); [26-2.ru](https://www.26-2.ru/art/357926-vznosy-ip-1-s-dohoda-svyshe-300-000-rubley)
- **Ozon Blogger.**
  - Referral/affiliate program launched at the end of 2025. It was opened to authors on VK and the MAX messenger (news of May 2026).
  - Any author can join regardless of audience size, but participation is for users registered as самозанятые.
  - Reward depends on category and reaches up to 50% of the purchase price.
  - To join, the author applies on the landing page, stating platform and tax status, and gets access to the blogger cabinet after moderation.
  - Sources: [Click.ru](https://blog.click.ru/market-news/na-ozon-poyavilas-partnerskaya-programma-dlya-avtorov-vkontakte-i-max/); [Sostav](https://www.sostav.ru/publication/ozon-zapustil-referalnuyu-programmu-dlya-avtorov-maksa-i-vkontakte-84046.html); [AdIndex, 25.05.2026](https://adindex.ru/news/digital/2026/05/25/345259.phtml); [ozon.ru/bloggers](https://www.ozon.ru/bloggers)
  - Another summary says access for ИП "will appear later", payouts are monthly with a minimum withdrawal of 500 ₽, and withdrawal requires самозанятый or ИП status. — [ozon.ru/bloggers](https://www.ozon.ru/bloggers); [Pampadu](https://pampadu.ru/blog/10266-kak-zarabotat-na-partnerkah-ozon-wildberries-aliexpress-i-yandeks-market/)
  - The same summary claims that "Ozon acts as tax agent and withholds 13% НДФЛ (or 6% for самозанятые)". This looks internally inconsistent: a самозанятый pays НПД themselves, and a tax agent cannot withhold НПД. Treat it as unreliable.
- **Wildberries.** WB's affiliate program is open to arbitrage marketers, bloggers, influencers, content makers and community owners. Registration as самозанятый, ООО or ИП is mandatory. — [Pampadu](https://pampadu.ru/blog/10266-kak-zarabotat-na-partnerkah-ozon-wildberries-aliexpress-i-yandeks-market/); [Affelist](https://affelist.ru/stati/referalnye-programmy-marketplejsov/)
- **Яндекс Маркет.** The referral program targets owners of Telegram channels, VK groups and other media with самозанятый status. There is no minimum subscriber count. — [PRO CPA](https://procpa.media/articles/partnerskaya-programma-yandeks-market-gajd-dlya-arbitrazhnikov-2026/); [Affelist](https://affelist.ru/stati/referalnye-programmy-marketplejsov/)
- **3% fee for bloggers.** Taxes for bloggers in 2026 combine the income-tax regime (НПД/УСН/НДФЛ) with the 3% advertising fee (see section 2). — [Контур](https://kontur-center.ru/news/extern/nalog-3-na-czifrovuyu-reklamu-kto-i-kak-perechislyaet-sbor-v-2026-godu/); [ПодборНалог](https://podbornalog.ru/blog/nalogi-blogera-2026)

### Inferences
- **Cost comparison at 1,000,000 ₽ a year of affiliate income from companies** (marketplaces, CPA networks):
  - НПД at 6% is about 60,000 ₽, somewhat less while the 10k deduction lasts.
  - ИП on УСН 6% is 60,000 ₽ tax, but it is reduced by contributions of 57,390 + 7,000. For an ИП without employees, the УСН tax can be reduced by 100% of own contributions (background rule, not verified here). The effective cost is roughly equal, with more paperwork.
  - Above 2.4 mln ₽ a year, НПД is unavailable and ИП/УСН becomes necessary. Above 20 mln ₽ in 2026, НДС applies (at reduced 5%/7% or general rate — not verified here).
- Programs that insist on самозанятый, ИП or ООО status (WB, Яндекс Маркет, Ozon Blogger) effectively exclude plain individuals. An individual without status would have to register НПД (free, via the «Мой налог» app) to participate.

### Gaps
- **Progressive НДФЛ.** Not verified in this session. Background (unverified): Law 176-ФЗ of 12.07.2024 sets from 1 Jan 2025: 13% up to 2.4 mln ₽; 15% for 2.4–5 mln ₽; 18% for 5–20 mln ₽; 20% for 20–50 mln ₽; 22% above 50 mln ₽. A plain individual receiving affiliate income from a Russian company would have НДФЛ withheld by the payer as tax agent, and the payer would also owe insurance contributions on a civil-law contract. Many CPA networks therefore prefer самозанятые/ИП.
- **НПД restrictions.** Could not verify whether агентские/посреднические договоры (common in affiliate contracts) conflict with НПД restrictions (ст.4 422-ФЗ bans intermediary activity under agency contracts), or ФНС guidance on affiliate income under НПД.
- **Bank referral bonuses** («Приведи друга»). Could not verify their taxability; searches were blocked by budget exhaustion. Background (unverified): Минфин/ФНС treat such bonuses as payment for services (attracting clients), so they are taxable. The bank either withholds НДФЛ as tax agent or reports non-withheld tax to the ФНС, and the individual pays by 1 December of the following year.
- **Cashback.** Could not verify the exemption for card cashback. Background (unverified): п.68 ст.217 НК exempts bonuses and cashback under loyalty programs unless they are payment for services or work, or are paid under programs where the customer provides a service.
- **Deposit interest.** Could not verify the non-taxable threshold for 2025 and 2026. Background (unverified): the threshold is 1 mln ₽ × the maximum key rate on the 1st of any month of the year. That gives 210,000 ₽ for 2025 (key rate 21%). For 2026 it is likely 160,000 ₽ if the 1 Jan 2026 rate of 16% was the year's maximum. Verify on nalog.gov.ru.
- **Fixed contributions for 2025.** Not verified for comparison. Background (unverified): 53,658 ₽.
- **CPA networks' accepted statuses.** No 2026 source retrieved on which statuses Admitad, Где Слон?, Leads.su, Advcake and others accept, or whether they pay plain individuals with НДФЛ withheld.

## 5. Consumer-protection and content risks: financial-services ads (bank products), banned categories, misleading promo codes

### Takeaway
Only general rules could be confirmed in this session. Any breach of the Law on Advertising is fined under ч.1 ст.14.3 КоАП (citizens 2,000–2,500 ₽; officials/ИП 4,000–20,000 ₽; legal entities 100,000–500,000 ₽). Liability extends to both advertiser and distributor, and ФАС is increasingly focused on internet ads. Specific financial-ad requirements and category bans could not be verified from sources.

### Cited Findings
- **General liability.** Breaches of the Law on Advertising by an advertiser, producer or distributor are fined under ч.1 ст.14.3 КоАП: citizens 2,000–2,500 ₽; officials 4,000–20,000 ₽; legal entities 100,000–500,000 ₽. — [КонсультантПлюс](https://www.consultant.ru/document/cons_doc_LAW_34661/2d50fc1c4013ea9ab20b8b2666c1650b1dc4c982/); [audit-it.ru](https://www.audit-it.ru/koap/14_3.html)
- **Shared liability.** Delegating to an agent does not relieve the advertiser. If the agent fails, both can be fined. — [Ветров и партнёры](https://vitvet.com/articles/koap/sostavy/shtraf-narushenie-zakona-reklame-14-3-2026/)
- **Enforcement focus.** Internet ads made up more than 40% of advertising-law violations found by ФАС in 2024–2025. — [Ветров и партнёры](https://vitvet.com/articles/koap/sostavy/shtraf-narushenie-zakona-reklame-14-3-2026/)

### Inferences
- An affiliate who promotes bank cards, deposits or loans acts as рекламораспространитель and, often, the producer of the post text. They share liability for missing mandatory disclosures and for misleading claims, for example "free card", "cashback up to X%" without conditions, or promo codes that do not work as advertised.

### Gaps
- **Financial-services ads (art. 28 of 38-ФЗ).** Not verified. Background (unverified):
  - ads must name the financial organization;
  - loan and credit-card ads must show the full credit cost (ПСК) range with formatting requirements;
  - deposit ads must state all conditions affecting yield;
  - ads must not promise yield where it is not guaranteed.
  Bank referral programs typically make partners use approved creatives.
- **Banned or restricted categories.** Not verified in this session. Background (unverified):
  - VPN and block-bypass tools (406-ФЗ, from 1 March 2024);
  - cryptocurrency and digital-currency offers (law of August 2024);
  - unlicensed gambling and betting;
  - online alcohol;
  - tobacco and nicotine products;
  - prescription medicines;
  - restrictions on БАДы and medical services.
- **Misleading ads and promo codes.** Not verified. Background (unverified): недостоверная реклама under ч.3 ст.5 38-ФЗ, and the Law on Protection of Consumers' Rights for the advertiser.
- No ФАС 2025–2026 cases on bloggers promoting bank products or marketplace promo codes were retrieved.

## 6. 2026 changes and pending bills relevant to bloggers and affiliate marketers

### Takeaway
The main changes in force for 2026 are:
- ЕРИР reporting limited to roughly one year (Sept 2025);
- the Instagram and blocked-resource ad ban (1 Sept 2025);
- a stable 3% ad fee with shifted 2026 payment dates;
- much lower УСН НДС thresholds (20 mln ₽ in 2026) under 425-ФЗ;
- higher ИП contributions (57,390 ₽);
- expansion of marketplace blogger programs to VK and MAX (Ozon Blogger, May 2026).

No enacted 2026 law specifically targeting affiliate marketers was found. НПД is fixed until 2028.

### Cited Findings
- **ЕРИР reporting limited in time.** Advertisers stop reporting ads older than one year. ЕРИР storage is reduced from 5 to 3 years (decree № 1427, September 2025; supersedes "perpetual" reporting). — [Кабельщик](https://www.cableman.ru/content/srok-otchetnosti-po-reklame-ogranichen-odnim-godom); [Эксперт](https://expert.ru/news/assotsiatsiya-blogerov-i-agentstv-dobilas-otmeny-vechnoy-otchetnosti-po-reklame/)
- **Blocked-resource ban.** Advertising on blocked and extremist-organization resources has been banned since 1 Sept 2025 (72-ФЗ). — [ГАРАНТ.РУ](https://www.garant.ru/hotlaw/federal/1807775/)
- **3% fee calendar.** 2026 payment dates are 5 March, 5 June, 7 September and 7 December 2026. — [Law.ru](https://www.law.ru/news/43713-v-2026-godu-srok-uplaty-reklamnogo-sbora-sdvinetsya-dvajdy)
- **УСН НДС threshold.** 20 mln ₽ from 1 Jan 2026 (425-ФЗ of 28.11.2025). — [Контур.Экстерн](https://www.kontur-extern.ru/info/81877-usn_i_nds)
- **НПД.** Unchanged in 2026; the regime is kept until 2028, and reform ideas (5% single rate, progression) are postponed to 2028. — [e-Контур](https://e-kontur.ru/enquiry/2657/otmenyat-li-npd)
- **ИП contributions.** 57,390 ₽ fixed for 2026. — [Regberry](https://www.regberry.ru/nalogooblozhenie/fiksirovannye-vznosy-ip-2026)
- **Ozon Blogger expansion.** Opened to VK and MAX authors (May 2026); самозанятые only; up to 50% commission. — [AdIndex](https://adindex.ru/news/digital/2026/05/25/345259.phtml); [Sostav](https://www.sostav.ru/publication/ozon-zapustil-referalnuyu-programmu-dlya-avtorov-maksa-i-vkontakte-84046.html)
- **Not an ad-fee change.** The March 2026 idea of a 3% levy on marketplaces for «Почта России» was not included in the Минцифры draft law. — [ComNews](https://www.comnews.ru/content/244419/2026-03-26/2026-w13/1008/mincifry-ne-vklyuchilo-zakonoproekt-normu-o-3-nom-sbore-marketpleysov-polzu-pochty-rossii)

### Inferences
- The regulatory direction is towards more transparency and platform control rather than lower costs:
  - identity registration for large pages;
  - ЕРИР data driving the 3% fee;
  - bans tied to blocking and extremism registers.
- The practical cost for a small affiliate is mostly compliance time: marking, reporting, the registry check, and the tax status. Direct fees are small (НПД 4–6%; the 3% fee is usually paid upstream by the network).
- The УСН НДС threshold cut matters only to large affiliate businesses (over 20 mln ₽ a year) but is a key 2026 change for ИП bloggers.

### Gaps
- Could not search for pending Госдума bills of 2026 on bloggers or affiliates: the search budget was exhausted. Examples to check: mandatory ИП/самозанятый status for bloggers, new КоАП fines for unregistered 10k+ pages, changes to the 3% fee, ad restrictions in messengers other than MAX.
- Could not verify the platform-economy law (Federal Law of 31.07.2025 № 289-ФЗ «О платформенной экономике», reportedly in force from 1 Oct 2025) or whether it affects marketplace affiliate partners.
- Could not verify the September 2026 state of the fine bands. No evidence of increases was found, but the search was limited.
