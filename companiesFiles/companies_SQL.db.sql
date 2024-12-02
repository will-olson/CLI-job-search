BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        link TEXT,
        indeed TEXT,
        favorite BOOLEAN,
        category TEXT
    );
CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        company_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(company_id) REFERENCES companies(id)
    );
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
INSERT INTO "companies" ("id","name","link","indeed","favorite","category") VALUES (1,'Walmart','https://www.linkedin.com/company/walmart/jobs/','https://www.indeed.com/cmp/Walmart',0,'IndustryLeaders'),
 (2,'BestBuy','https://www.linkedin.com/company/best-buy/jobs/','https://www.indeed.com/cmp/Best-Buy',0,'IndustryLeaders'),
 (3,'Home Depot','https://www.linkedin.com/company/the-home-depot/jobs/','https://www.indeed.com/cmp/The-Home-Depot',0,'IndustryLeaders'),
 (4,'Target','https://www.linkedin.com/company/target/jobs/','https://www.indeed.com/cmp/Target',0,'IndustryLeaders'),
 (5,'Costco','https://www.linkedin.com/company/costco-wholesale/jobs/','https://www.indeed.com/cmp/Costco-Wholesale',0,'IndustryLeaders'),
 (6,'United Airlines','https://www.linkedin.com/company/united-airlines/jobs/','https://www.indeed.com/cmp/United-Airlines',0,'IndustryLeaders'),
 (7,'Fedex','https://www.linkedin.com/company/fedex/jobs/','https://www.indeed.com/cmp/FedEx',0,'IndustryLeaders'),
 (8,'Aflac','https://www.linkedin.com/company/aflac/jobs/','https://www.indeed.com/cmp/Aflac',0,'IndustryLeaders'),
 (9,'GEICO','https://www.linkedin.com/company/geico/jobs/','https://www.indeed.com/cmp/Geico',0,'IndustryLeaders'),
 (10,'Kroger','https://www.linkedin.com/company/kroger/jobs/','https://www.indeed.com/cmp/Kroger',0,'IndustryLeaders'),
 (11,'Boeing','https://www.linkedin.com/company/boeing/jobs/','https://www.indeed.com/cmp/Boeing',0,'IndustryLeaders'),
 (12,'Tesla','https://www.linkedin.com/company/tesla-motors/jobs/','https://www.indeed.com/cmp/Tesla',0,'IndustryLeaders'),
 (13,'The RealReal','https://www.linkedin.com/company/the-realreal/jobs/','https://www.indeed.com/cmp/The-Realreal',0,'IndustryLeaders'),
 (14,'Adobe','https://www.linkedin.com/company/adobe/jobs/','https://www.indeed.com/cmp/Adobe',0,'BigTech'),
 (15,'Microsoft','https://www.linkedin.com/company/microsoft/jobs/','https://www.indeed.com/cmp/Microsoft',0,'BigTech'),
 (16,'Dropbox','https://www.linkedin.com/company/dropbox/jobs/','https://www.indeed.com/cmp/Dropbox-ab4b15a9',0,'BigTech'),
 (17,'Meta','https://www.linkedin.com/company/meta/jobs/','https://www.indeed.com/cmp/Meta-dd1502f2',0,'BigTech'),
 (18,'Google','https://www.linkedin.com/company/google/jobs/','https://www.indeed.com/cmp/Google',0,'BigTech'),
 (19,'Apple','https://www.linkedin.com/company/apple/jobs/','https://www.indeed.com/cmp/Apple',0,'BigTech'),
 (20,'Airbnb','https://www.linkedin.com/company/airbnb/jobs/','https://www.indeed.com/cmp/Airbnb',0,'BigTech'),
 (21,'Uber','https://www.linkedin.com/company/uber-com/jobs/','https://www.indeed.com/cmp/Uber',0,'BigTech'),
 (22,'LinkedIn','https://www.linkedin.com/company/linkedin/jobs/','https://www.indeed.com/cmp/Linkedin',0,'BigTech'),
 (23,'Cruise','https://www.linkedin.com/company/getcruise/jobs/','https://www.indeed.com/cmp/Cruise-fc3bd24b',0,'BigTech'),
 (24,'NVIDIA','https://www.linkedin.com/company/nvidia/jobs/','https://www.indeed.com/cmp/Nvidia',0,'BigTech'),
 (25,'Snap','https://www.linkedin.com/company/snap-inc-co/jobs/','https://www.indeed.com/cmp/Snap-Inc.',0,'BigTech'),
 (26,'Zillow','https://www.linkedin.com/company/zillow/jobs/','https://www.indeed.com/cmp/Zillow',0,'BigTech'),
 (27,'X','https://careers.x.com/','https://www.indeed.com/cmp/Twitter',0,'BigTech'),
 (28,'Netflix','https://www.linkedin.com/company/netflix/jobs/','https://www.indeed.com/cmp/Netflix',0,'Media'),
 (29,'Spotify','https://www.linkedin.com/company/spotify/jobs/','https://www.indeed.com/cmp/Spotify',0,'Media'),
 (30,'SoundCloud','https://www.linkedin.com/company/soundcloud/jobs/','https://www.indeed.com/cmp/Soundcloud',0,'Media'),
 (31,'Walt Disney Company','https://www.linkedin.com/company/the-walt-disney-company/jobs/','https://www.indeed.com/cmp/The-Walt-Disney-Company',0,'Media'),
 (32,'Warner Bros. Discovery','https://www.linkedin.com/company/warner-bros-discovery/jobs/','https://www.indeed.com/cmp/Warner-Bros.-Discovery',0,'Media'),
 (33,'Paramount Global','https://www.linkedin.com/company/paramount/jobs/','https://www.indeed.com/cmp/Paramount-66ac57f4',0,'Media'),
 (34,'Scale AI','https://www.linkedin.com/company/scaleai/jobs/','https://www.indeed.com/cmp/Scale-AI',0,'AI'),
 (35,'Anthropic','https://www.linkedin.com/company/anthropicresearch/jobs/','https://www.indeed.com/cmp/Anthropic',0,'AI'),
 (36,'OpenAI','https://www.linkedin.com/company/openai/jobs/','https://www.indeed.com/cmp/Openai',0,'AI'),
 (37,'Figma','https://www.linkedin.com/company/figma/jobs/','https://www.indeed.com/cmp/Figma',0,'MarketingSaaS'),
 (38,'Iterable','https://www.linkedin.com/company/iterable/jobs/','https://www.indeed.com/cmp/Iterable',0,'MarketingSaaS'),
 (39,'Miro','https://www.linkedin.com/company/mirohq/jobs/','https://www.indeed.com/cmp/Miro-3b3ebbc2',0,'MarketingSaaS'),
 (40,'Mixpanel','https://www.linkedin.com/company/mixpanel-inc-/jobs/','https://www.indeed.com/cmp/Mixpanel',0,'MarketingSaaS'),
 (41,'Airtable','https://www.linkedin.com/company/airtable/jobs/','https://www.indeed.com/cmp/Airtable',0,'MarketingSaaS'),
 (42,'Smartly','https://www.linkedin.com/company/smartly-io/jobs/','https://www.indeed.com/cmp/Smartly',0,'MarketingSaaS'),
 (43,'Canva','https://www.linkedin.com/company/canva/jobs/','https://www.indeed.com/cmp/Canva',0,'MarketingSaaS'),
 (44,'Boston Scientific','https://www.linkedin.com/company/boston-scientific/jobs/','https://www.indeed.com/cmp/Boston-Scientific',0,'Healthcare'),
 (45,'Amgen','https://www.linkedin.com/company/amgen/jobs/','https://www.indeed.com/cmp/Amgen',0,'Healthcare'),
 (46,'Johnson & Johnson','https://www.linkedin.com/company/johnson-&-johnson/jobs/','https://www.indeed.com/cmp/Johnson-&-Johnson',0,'Healthcare'),
 (47,'Pfizer','https://www.linkedin.com/company/pfizer/jobs/','https://www.indeed.com/cmp/Pfizer',0,'Healthcare'),
 (48,'Roche','https://www.linkedin.com/company/roche/jobs/','https://www.indeed.com/cmp/Roche',0,'Healthcare'),
 (49,'UnitedHealthcare','https://www.linkedin.com/company/unitedhealthcare/jobs/','https://www.indeed.com/cmp/UnitedHealthcare',0,'Healthcare'),
 (50,'Philips Healthcare','https://www.linkedin.com/company/philips/jobs/','https://www.indeed.com/cmp/Philips-Healthcare',0,'Healthcare'),
 (51,'Align Technology','https://www.linkedin.com/company/align-technology/jobs/','https://www.indeed.com/cmp/Align-Technology',0,'Healthcare'),
 (52,'VISA','https://www.linkedin.com/company/visa/jobs/','https://www.indeed.com/cmp/Visa',0,'Fintech'),
 (53,'Paypal','https://www.linkedin.com/company/paypal/jobs/','https://www.indeed.com/cmp/PayPal',0,'Fintech'),
 (54,'Square','https://www.linkedin.com/company/joinsquare/jobs/','https://www.indeed.com/cmp/Square',0,'Fintech'),
 (55,'Robinhood','https://www.linkedin.com/company/robinhood/jobs/','https://www.indeed.com/cmp/Robinhood',0,'Fintech'),
 (56,'Chime','https://www.linkedin.com/company/chime-card/jobs/','https://www.indeed.com/cmp/Chime-5',0,'Fintech'),
 (57,'Stripe','https://www.linkedin.com/company/stripe/jobs/','https://www.indeed.com/cmp/Stripe',0,'Fintech'),
 (58,'Plaid','https://www.linkedin.com/company/plaid-/jobs/','https://www.indeed.com/cmp/Plaid-3',0,'Fintech'),
 (59,'Adyen','https://www.linkedin.com/company/adyen/jobs/','https://www.indeed.com/cmp/Adyen',0,'Fintech'),
 (60,'Brex','https://www.linkedin.com/company/brexhq/jobs/','https://www.indeed.com/cmp/Brex-5',0,'Fintech'),
 (61,'Goldman Sachs','https://www.linkedin.com/company/goldman-sachs/jobs/','https://www.indeed.com/cmp/Goldman-Sachs',0,'Finance'),
 (62,'JPMorgan','https://www.linkedin.com/company/jpmorgan/jobs/','https://www.indeed.com/cmp/JPMorgan',0,'Finance'),
 (63,'Citadel','https://www.linkedin.com/company/citadel-llc/jobs/','https://www.indeed.com/cmp/Citadel-Securities',0,'Finance'),
 (64,'Jane Street','https://www.linkedin.com/company/jane-street-global/jobs/','https://www.indeed.com/cmp/Jane-Street-4',0,'Finance'),
 (65,'Hudson River Trading','https://www.linkedin.com/company/hudson-river-trading/jobs/','https://www.indeed.com/cmp/Hudson-River-Trading',0,'Finance'),
 (66,'Arrowstreet Capital','https://www.linkedin.com/company/arrowstreet-capital/jobs/','https://www.indeed.com/cmp/Arrowstreet-Capital',0,'Finance'),
 (67,'Two Sigma','https://www.linkedin.com/company/two-sigma-investments/jobs/','https://www.indeed.com/cmp/Two-Sigma',0,'Finance'),
 (68,'Five Rings','https://www.linkedin.com/company/fiverings/jobs/','https://fiverings.com/careers/',0,'Finance'),
 (69,'Optiver','https://www.linkedin.com/company/optiver/jobs/','https://www.indeed.com/cmp/Optiver',0,'Finance'),
 (70,'DRW','https://www.linkedin.com/company/drw/jobs/','https://www.indeed.com/cmp/DRW',0,'Finance'),
 (71,'IMC Trading','https://www.linkedin.com/company/imc-financial-markets/jobs/','https://www.indeed.com/cmp/Imc-Financial-Markets',0,'Finance'),
 (72,'Autodesk','https://www.linkedin.com/company/autodesk/jobs/','https://www.indeed.com/cmp/Autodesk',0,'B2BSaaS'),
 (73,'Databricks','https://www.linkedin.com/company/databricks/jobs/','https://www.indeed.com/cmp/Databricks',0,'B2BSaaS'),
 (74,'HubSpot','https://www.linkedin.com/company/hubspot/jobs/','https://www.indeed.com/cmp/HubSpot',0,'B2BSaaS'),
 (75,'Okta','https://www.linkedin.com/company/okta-inc-/jobs/','https://www.indeed.com/cmp/Okta',0,'B2BSaaS'),
 (76,'Salesforce','https://www.linkedin.com/company/salesforce/jobs/','https://www.indeed.com/cmp/Salesforce',0,'B2BSaaS'),
 (77,'ServiceTitan','https://www.linkedin.com/company/servicetitan/jobs/','https://www.indeed.com/cmp/ServiceTitan',0,'B2BSaaS'),
 (78,'Monday.com','https://www.linkedin.com/company/mondaydotcom/jobs/','https://www.indeed.com/cmp/Monday.com',0,'B2BSaaS'),
 (79,'Gong','https://www.linkedin.com/company/gong-io/jobs/','https://www.indeed.com/cmp/Gong-7',0,'B2BSaaS'),
 (80,'Toast','https://www.linkedin.com/company/toast-inc/jobs/','https://www.indeed.com/cmp/Toast,-Inc',0,'B2BSaaS'),
 (84,'Squarespace','https://www.linkedin.com/company/squarespace/jobs/','https://www.indeed.com/cmp/Squarespace',0,'MarketingSaaS'),
 (86,'TestB','https://www.linkedin.com/company/testB','https://www.indeed.com/cmp/testB',0,'AI'),
 (87,'TestC','https://www.linkedin.com/company/testC','https://www.indeed.com/cmp/testC',0,'AI');
INSERT INTO "favorites" ("id","user_id","company_id") VALUES (1,1,17),
 (2,3,20),
 (3,2,41),
 (4,5,53),
 (5,4,81),
 (6,4,17);
INSERT INTO "users" ("id","name") VALUES (1,'Ethan'),
 (2,'Hannah'),
 (3,'Maddie'),
 (4,'Bill'),
 (5,'William');
COMMIT;