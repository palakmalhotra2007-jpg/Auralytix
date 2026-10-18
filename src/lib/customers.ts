import type { Customer, CustomerSignal } from './types';
import { API_BASE } from './apiConfig';

// 50 Real Scored Customer Accounts seeded from Database and SVM Churn Model
export const customers: Customer[] = [
  {
    "id": "c_001",
    "name": "Maya Chen",
    "company": "Northwind Robotics",
    "email": "maya@northwind.io",
    "tier": "Enterprise",
    "plan_value": 12000.0,
    "avatarHue": 0,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.74,
        "display": "74% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.25,
        "display": "2 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.73,
        "display": "0.73"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.76,
        "display": "76%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 1980,
    "lastActiveDays": 4
  },
  {
    "id": "c_002",
    "name": "Diego Alvarez",
    "company": "Lumen Health",
    "email": "diego@lumenhealth.com",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 37,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.84,
        "display": "83% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.25,
        "display": "2 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.83,
        "display": "0.83"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.85,
        "display": "85%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.5,
        "display": "3/6 steps"
      }
    ],
    "joinedDays": 420,
    "lastActiveDays": 2
  },
  {
    "id": "c_003",
    "name": "Priya Nair",
    "company": "Atlas Freight",
    "email": "priya@atlasfreight.co",
    "tier": "Growth",
    "plan_value": 4500.0,
    "avatarHue": 74,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.41,
        "display": "41% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.62,
        "display": "5 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.37,
        "display": "0.37"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.45,
        "display": "45%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 1.0,
        "display": "flagged"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.67,
        "display": "4/6 steps"
      }
    ],
    "joinedDays": 510,
    "lastActiveDays": 9
  },
  {
    "id": "c_004",
    "name": "Sam Okafor",
    "company": "Brightwave Media",
    "email": "sam@brightwave.tv",
    "tier": "Enterprise",
    "plan_value": 12000.0,
    "avatarHue": 111,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.96,
        "display": "95% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.0,
        "display": "0 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.95,
        "display": "0.95"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.96,
        "display": "96%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 2010,
    "lastActiveDays": 1
  },
  {
    "id": "c_005",
    "name": "Hana Kobayashi",
    "company": "Vertex Labs",
    "email": "hana@vertexlabs.ai",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 148,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.58,
        "display": "58% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.5,
        "display": "4 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.56,
        "display": "0.56"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.61,
        "display": "61%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.17,
        "display": "1/6 steps"
      }
    ],
    "joinedDays": 30,
    "lastActiveDays": 6
  },
  {
    "id": "c_006",
    "name": "Lucas Pereira",
    "company": "Cedar & Co",
    "email": "lucas@cedarco.com",
    "tier": "Enterprise",
    "plan_value": 12000.0,
    "avatarHue": 185,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.88,
        "display": "87% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.12,
        "display": "1 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.87,
        "display": "0.87"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.89,
        "display": "89%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 1770,
    "lastActiveDays": 1
  },
  {
    "id": "c_007",
    "name": "Aaliyah Brooks",
    "company": "Skyline Energy",
    "email": "aaliyah@skyline.energy",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 222,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.7,
        "display": "70% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.38,
        "display": "3 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.68,
        "display": "0.68"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.72,
        "display": "72%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 1050,
    "lastActiveDays": 4
  },
  {
    "id": "c_008",
    "name": "Theo M\u00fcller",
    "company": "Quantum Gear",
    "email": "theo@quantumgear.de",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 259,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.87,
        "display": "86% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.12,
        "display": "1 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.86,
        "display": "0.86"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.87,
        "display": "87%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.83,
        "display": "5/6 steps"
      }
    ],
    "joinedDays": 660,
    "lastActiveDays": 2
  },
  {
    "id": "c_009",
    "name": "Ines Garcia",
    "company": "Harbor Pay",
    "email": "ines@harborpay.io",
    "tier": "Growth",
    "plan_value": 4500.0,
    "avatarHue": 296,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.98,
        "display": "97% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.0,
        "display": "0 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.95,
        "display": "0.95"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.96,
        "display": "96%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 2160,
    "lastActiveDays": 1
  },
  {
    "id": "c_010",
    "name": "Ravi Shankar",
    "company": "Nimbus Cloud",
    "email": "ravi@nimbus.cloud",
    "tier": "Growth",
    "plan_value": 4500.0,
    "avatarHue": 333,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.42,
        "display": "42% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.62,
        "display": "5 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.38,
        "display": "0.38"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.46,
        "display": "46%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 1.0,
        "display": "flagged"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 780,
    "lastActiveDays": 9
  },
  {
    "id": "c_011",
    "name": "Greta Lindholm",
    "company": "Polar Foods",
    "email": "greta@polarfoods.se",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 10,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.4,
        "display": "39% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.75,
        "display": "6 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.36,
        "display": "0.36"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.44,
        "display": "44%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 1.0,
        "display": "flagged"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.17,
        "display": "1/6 steps"
      }
    ],
    "joinedDays": 180,
    "lastActiveDays": 9
  },
  {
    "id": "c_012",
    "name": "Omar Haddad",
    "company": "Sable Logistics",
    "email": "omar@sablelog.com",
    "tier": "Growth",
    "plan_value": 4500.0,
    "avatarHue": 47,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.38,
        "display": "37% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.75,
        "display": "6 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.33,
        "display": "0.33"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.42,
        "display": "42%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 1.0,
        "display": "flagged"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.5,
        "display": "3/6 steps"
      }
    ],
    "joinedDays": 360,
    "lastActiveDays": 9
  },
  {
    "id": "c_013",
    "name": "Elena Rostova",
    "company": "Apex Dynamics",
    "email": "elena@apexdynamics.com",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 84,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.93,
        "display": "93% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.12,
        "display": "1 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.93,
        "display": "0.93"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.94,
        "display": "94%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 1830,
    "lastActiveDays": 1
  },
  {
    "id": "c_014",
    "name": "Marcus Vance",
    "company": "BlueShift AI",
    "email": "marcus@blueshift.ai",
    "tier": "Growth",
    "plan_value": 4500.0,
    "avatarHue": 121,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.36,
        "display": "35% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.75,
        "display": "6 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.31,
        "display": "0.31"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.4,
        "display": "40%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 1.0,
        "display": "flagged"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.17,
        "display": "1/6 steps"
      }
    ],
    "joinedDays": 90,
    "lastActiveDays": 10
  },
  {
    "id": "c_015",
    "name": "Sophia Sterling",
    "company": "Strata Capital",
    "email": "sophia@stratacap.com",
    "tier": "Growth",
    "plan_value": 4500.0,
    "avatarHue": 158,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.44,
        "display": "44% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.62,
        "display": "5 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.41,
        "display": "0.41"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.48,
        "display": "48%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 1.0,
        "display": "flagged"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.33,
        "display": "2/6 steps"
      }
    ],
    "joinedDays": 300,
    "lastActiveDays": 8
  },
  {
    "id": "c_016",
    "name": "Kenji Sato",
    "company": "Vanguard Health",
    "email": "kenji@vanguardhealth.jp",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 195,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.61,
        "display": "61% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.5,
        "display": "4 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.59,
        "display": "0.59"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.64,
        "display": "64%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 1320,
    "lastActiveDays": 6
  },
  {
    "id": "c_017",
    "name": "Clara Dupont",
    "company": "Zenith Networks",
    "email": "clara@zenithnet.co",
    "tier": "Growth",
    "plan_value": 4500.0,
    "avatarHue": 232,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.98,
        "display": "97% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.0,
        "display": "0 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.95,
        "display": "0.95"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.96,
        "display": "96%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 2160,
    "lastActiveDays": 1
  },
  {
    "id": "c_018",
    "name": "Liam O'Connor",
    "company": "Cascade Analytics",
    "email": "liam@cascadeanalytics.io",
    "tier": "Enterprise",
    "plan_value": 12000.0,
    "avatarHue": 269,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.96,
        "display": "95% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.0,
        "display": "0 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.95,
        "display": "0.95"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.96,
        "display": "96%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 2160,
    "lastActiveDays": 1
  },
  {
    "id": "c_019",
    "name": "Tariq Mansoor",
    "company": "Frontier Defense",
    "email": "tariq@frontierdefense.ae",
    "tier": "Enterprise",
    "plan_value": 12000.0,
    "avatarHue": 306,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.84,
        "display": "84% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.12,
        "display": "1 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.83,
        "display": "0.83"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.85,
        "display": "85%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 1260,
    "lastActiveDays": 2
  },
  {
    "id": "c_020",
    "name": "Ananya Sharma",
    "company": "Meridian Biotech",
    "email": "ananya@meridianbio.in",
    "tier": "Enterprise",
    "plan_value": 12000.0,
    "avatarHue": 343,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.49,
        "display": "49% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.62,
        "display": "5 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.46,
        "display": "0.46"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.52,
        "display": "52%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 1.0,
        "display": "flagged"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 900,
    "lastActiveDays": 8
  },
  {
    "id": "c_021",
    "name": "Charlie Zhang",
    "company": "Pulse Gaming",
    "email": "charlie@pulsegame.tv",
    "tier": "Enterprise",
    "plan_value": 12000.0,
    "avatarHue": 20,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.36,
        "display": "36% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.75,
        "display": "6 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.32,
        "display": "0.32"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.41,
        "display": "41%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 1.0,
        "display": "flagged"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.17,
        "display": "1/6 steps"
      }
    ],
    "joinedDays": 60,
    "lastActiveDays": 10
  },
  {
    "id": "c_022",
    "name": "Astrid Lind",
    "company": "Solstice Solar",
    "email": "astrid@solsticesolar.no",
    "tier": "Growth",
    "plan_value": 4500.0,
    "avatarHue": 57,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.41,
        "display": "40% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.75,
        "display": "6 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.37,
        "display": "0.37"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.45,
        "display": "45%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 1.0,
        "display": "flagged"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.5,
        "display": "3/6 steps"
      }
    ],
    "joinedDays": 450,
    "lastActiveDays": 9
  },
  {
    "id": "c_023",
    "name": "Mateo Silva",
    "company": "AeroStream",
    "email": "mateo@aerostream.aero",
    "tier": "Growth",
    "plan_value": 4500.0,
    "avatarHue": 94,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.4,
        "display": "40% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.75,
        "display": "6 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.36,
        "display": "0.36"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.44,
        "display": "44%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 1.0,
        "display": "flagged"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.5,
        "display": "3/6 steps"
      }
    ],
    "joinedDays": 390,
    "lastActiveDays": 9
  },
  {
    "id": "c_024",
    "name": "Zoe Bennett",
    "company": "Prism Security",
    "email": "zoe@prismsec.tech",
    "tier": "Growth",
    "plan_value": 4500.0,
    "avatarHue": 131,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.36,
        "display": "36% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.75,
        "display": "6 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.32,
        "display": "0.32"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.41,
        "display": "41%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 1.0,
        "display": "flagged"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.17,
        "display": "1/6 steps"
      }
    ],
    "joinedDays": 30,
    "lastActiveDays": 10
  },
  {
    "id": "c_025",
    "name": "Viktor Kozlov",
    "company": "Ironclad Logistics",
    "email": "viktor@ironcladlog.ru",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 168,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.62,
        "display": "62% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.5,
        "display": "4 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.6,
        "display": "0.60"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.65,
        "display": "65%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.17,
        "display": "1/6 steps"
      }
    ],
    "joinedDays": 180,
    "lastActiveDays": 6
  },
  {
    "id": "c_026",
    "name": "Nadia Fassi",
    "company": "Beacon Commerce",
    "email": "nadia@beaconcommerce.com",
    "tier": "Growth",
    "plan_value": 4500.0,
    "avatarHue": 205,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.88,
        "display": "87% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.12,
        "display": "1 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.87,
        "display": "0.87"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.89,
        "display": "89%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 930,
    "lastActiveDays": 1
  },
  {
    "id": "c_027",
    "name": "Hugo Laurent",
    "company": "Catalyst Labs",
    "email": "hugo@catalystlabs.fr",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 242,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.94,
        "display": "94% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.12,
        "display": "1 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.94,
        "display": "0.94"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.95,
        "display": "95%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 1710,
    "lastActiveDays": 1
  },
  {
    "id": "c_028",
    "name": "Sienna Miller",
    "company": "Kinetix Fitness",
    "email": "sienna@kinetixfit.com",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 279,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.4,
        "display": "40% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.75,
        "display": "6 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.36,
        "display": "0.36"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.44,
        "display": "44%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 1.0,
        "display": "flagged"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.33,
        "display": "2/6 steps"
      }
    ],
    "joinedDays": 240,
    "lastActiveDays": 9
  },
  {
    "id": "c_029",
    "name": "Arjun Patel",
    "company": "Hyperion Compute",
    "email": "arjun@hyperioncomp.com",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 316,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.64,
        "display": "64% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.38,
        "display": "3 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.62,
        "display": "0.62"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.67,
        "display": "67%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.5,
        "display": "3/6 steps"
      }
    ],
    "joinedDays": 390,
    "lastActiveDays": 5
  },
  {
    "id": "c_030",
    "name": "Fatima Al-Hassan",
    "company": "Oasis Renewable",
    "email": "fatima@oasisrenew.com",
    "tier": "Growth",
    "plan_value": 4500.0,
    "avatarHue": 353,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.35,
        "display": "35% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.75,
        "display": "6 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.31,
        "display": "0.31"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.4,
        "display": "40%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 1.0,
        "display": "flagged"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.17,
        "display": "1/6 steps"
      }
    ],
    "joinedDays": 30,
    "lastActiveDays": 10
  },
  {
    "id": "c_031",
    "name": "Gabriel Costa",
    "company": "Nova Genomics",
    "email": "gabriel@novagenomics.br",
    "tier": "Enterprise",
    "plan_value": 12000.0,
    "avatarHue": 30,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.78,
        "display": "77% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.25,
        "display": "2 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.76,
        "display": "0.76"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.79,
        "display": "79%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 810,
    "lastActiveDays": 3
  },
  {
    "id": "c_032",
    "name": "Olivia Hughes",
    "company": "Crestview Media",
    "email": "olivia@crestview.co.uk",
    "tier": "Enterprise",
    "plan_value": 12000.0,
    "avatarHue": 67,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.37,
        "display": "37% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.75,
        "display": "6 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.33,
        "display": "0.33"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.41,
        "display": "41%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 1.0,
        "display": "flagged"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.33,
        "display": "2/6 steps"
      }
    ],
    "joinedDays": 240,
    "lastActiveDays": 10
  },
  {
    "id": "c_033",
    "name": "Dmitri Volkov",
    "company": "Titanium Cloud",
    "email": "dmitri@titaniumcloud.ee",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 104,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.79,
        "display": "79% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.25,
        "display": "2 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.78,
        "display": "0.78"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.8,
        "display": "80%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.5,
        "display": "3/6 steps"
      }
    ],
    "joinedDays": 390,
    "lastActiveDays": 3
  },
  {
    "id": "c_034",
    "name": "Amelia Rossi",
    "company": "Summit Hospitality",
    "email": "amelia@summithotels.ch",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 141,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.56,
        "display": "56% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.5,
        "display": "4 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.53,
        "display": "0.53"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.59,
        "display": "59%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.17,
        "display": "1/6 steps"
      }
    ],
    "joinedDays": 30,
    "lastActiveDays": 7
  },
  {
    "id": "c_035",
    "name": "Khalil Qasim",
    "company": "Aegis Cyber",
    "email": "khalil@aegiscyber.qa",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 178,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.95,
        "display": "94% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.0,
        "display": "0 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.94,
        "display": "0.94"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.95,
        "display": "95%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 2160,
    "lastActiveDays": 1
  },
  {
    "id": "c_036",
    "name": "Yuki Tanaka",
    "company": "Cobalt Robotics",
    "email": "yuki@cobaltrobotics.jp",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 215,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.66,
        "display": "66% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.38,
        "display": "3 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.64,
        "display": "0.64"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.68,
        "display": "68%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.67,
        "display": "4/6 steps"
      }
    ],
    "joinedDays": 480,
    "lastActiveDays": 5
  },
  {
    "id": "c_037",
    "name": "Sebastian Weber",
    "company": "Echo Financial",
    "email": "sebastian@echofin.de",
    "tier": "Growth",
    "plan_value": 4500.0,
    "avatarHue": 252,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.98,
        "display": "97% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.0,
        "display": "0 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.95,
        "display": "0.95"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.96,
        "display": "96%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 2160,
    "lastActiveDays": 1
  },
  {
    "id": "c_038",
    "name": "Leila Haddad",
    "company": "Vortex Energy",
    "email": "leila@vortexenergy.ca",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 289,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.86,
        "display": "86% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.12,
        "display": "1 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.85,
        "display": "0.85"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.87,
        "display": "87%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 930,
    "lastActiveDays": 2
  },
  {
    "id": "c_039",
    "name": "Owen Wright",
    "company": "Horizon Space",
    "email": "owen@horizonspace.io",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 326,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.91,
        "display": "91% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.12,
        "display": "1 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.91,
        "display": "0.91"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.92,
        "display": "92%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 1440,
    "lastActiveDays": 1
  },
  {
    "id": "c_040",
    "name": "Valeria Morales",
    "company": "Optima Pharma",
    "email": "valeria@optimapharma.es",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 3,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.79,
        "display": "78% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.25,
        "display": "2 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.77,
        "display": "0.77"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.8,
        "display": "80%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.5,
        "display": "3/6 steps"
      }
    ],
    "joinedDays": 360,
    "lastActiveDays": 3
  },
  {
    "id": "c_041",
    "name": "Kwame Mensah",
    "company": "Terra Agriculture",
    "email": "kwame@terraagri.gh",
    "tier": "Growth",
    "plan_value": 4500.0,
    "avatarHue": 40,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.39,
        "display": "39% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.75,
        "display": "6 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.35,
        "display": "0.35"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.43,
        "display": "43%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 1.0,
        "display": "flagged"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.33,
        "display": "2/6 steps"
      }
    ],
    "joinedDays": 300,
    "lastActiveDays": 9
  },
  {
    "id": "c_042",
    "name": "Freja Nielsen",
    "company": "Labyrinth Security",
    "email": "freja@labyrinthsec.dk",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 77,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.43,
        "display": "42% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.62,
        "display": "5 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.39,
        "display": "0.39"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.47,
        "display": "47%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 1.0,
        "display": "flagged"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.17,
        "display": "1/6 steps"
      }
    ],
    "joinedDays": 210,
    "lastActiveDays": 9
  },
  {
    "id": "c_043",
    "name": "Dante Moretti",
    "company": "Equinox Media",
    "email": "dante@equinoxmedia.it",
    "tier": "Growth",
    "plan_value": 4500.0,
    "avatarHue": 114,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.55,
        "display": "54% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.5,
        "display": "4 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.52,
        "display": "0.52"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.58,
        "display": "57%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 1530,
    "lastActiveDays": 7
  },
  {
    "id": "c_044",
    "name": "Elizabeth Taylor",
    "company": "Starlight SaaS",
    "email": "elizabeth@starlightapp.com",
    "tier": "Growth",
    "plan_value": 4500.0,
    "avatarHue": 151,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.97,
        "display": "97% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.0,
        "display": "0 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.95,
        "display": "0.95"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.96,
        "display": "96%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 2130,
    "lastActiveDays": 1
  },
  {
    "id": "c_045",
    "name": "Connor MacLeod",
    "company": "Nautilus Marine",
    "email": "connor@nautilusmarine.au",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 188,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.58,
        "display": "58% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.5,
        "display": "4 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.55,
        "display": "0.55"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.61,
        "display": "61%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.17,
        "display": "1/6 steps"
      }
    ],
    "joinedDays": 30,
    "lastActiveDays": 6
  },
  {
    "id": "c_046",
    "name": "Mei-Ling Zhou",
    "company": "Pinnacle AI",
    "email": "mei@pinnacleai.sg",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 225,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.56,
        "display": "56% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.5,
        "display": "4 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.53,
        "display": "0.53"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.59,
        "display": "59%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 1.0,
        "display": "flagged"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.17,
        "display": "1/6 steps"
      }
    ],
    "joinedDays": 30,
    "lastActiveDays": 7
  },
  {
    "id": "c_047",
    "name": "Lars Berg",
    "company": "Solaris CleanTech",
    "email": "lars@solarisclean.se",
    "tier": "Growth",
    "plan_value": 4500.0,
    "avatarHue": 262,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.94,
        "display": "94% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.12,
        "display": "1 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.94,
        "display": "0.94"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.94,
        "display": "94%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 1680,
    "lastActiveDays": 1
  },
  {
    "id": "c_048",
    "name": "Nadine De Jong",
    "company": "Cipher Systems",
    "email": "nadine@ciphersys.nl",
    "tier": "Enterprise",
    "plan_value": 12000.0,
    "avatarHue": 299,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.47,
        "display": "47% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.62,
        "display": "5 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.44,
        "display": "0.44"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.51,
        "display": "51%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 1.0,
        "display": "flagged"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 1110,
    "lastActiveDays": 8
  },
  {
    "id": "c_049",
    "name": "Carlos Mendoza",
    "company": "Aura Health",
    "email": "carlos@aurahealth.mx",
    "tier": "Starter",
    "plan_value": 990.0,
    "avatarHue": 336,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.87,
        "display": "86% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.12,
        "display": "1 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.86,
        "display": "0.86"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.88,
        "display": "88%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 0.83,
        "display": "5/6 steps"
      }
    ],
    "joinedDays": 690,
    "lastActiveDays": 2
  },
  {
    "id": "c_050",
    "name": "Rachel Adams",
    "company": "Apex Global",
    "email": "rachel@apexglobal.com",
    "tier": "Enterprise",
    "plan_value": 12000.0,
    "avatarHue": 13,
    "signals": [
      {
        "key": "login_frequency",
        "label": "Login frequency",
        "value": 0.79,
        "display": "79% vs 30d"
      },
      {
        "key": "support_tickets",
        "label": "Support tickets",
        "value": 0.25,
        "display": "2 open"
      },
      {
        "key": "sentiment_score",
        "label": "Sentiment score",
        "value": 0.78,
        "display": "0.78"
      },
      {
        "key": "feature_adoption",
        "label": "Feature adoption",
        "value": 0.81,
        "display": "81%"
      },
      {
        "key": "billing_anomaly",
        "label": "Billing anomaly",
        "value": 0.0,
        "display": "clean"
      },
      {
        "key": "onboarding_progress",
        "label": "Onboarding progress",
        "value": 1.0,
        "display": "6/6 steps"
      }
    ],
    "joinedDays": 1920,
    "lastActiveDays": 3
  }
];

export let liveCustomersCache: Customer[] = [...customers];

export async function fetchCustomers(): Promise<Customer[]> {
  try {
    const res = await fetch(`${API_BASE}/api/customers`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    if (Array.isArray(data) && data.length > 0) {
      liveCustomersCache = data.map((c: any) => ({
        id: c.id,
        name: c.name,
        company: c.company,
        email: c.email,
        tier: c.tier,
        plan_value: c.plan_value,
        avatarHue: c.avatarHue ?? c.avatar_hue ?? 180,
        signals: c.signals ?? [],
        joinedDays: c.joinedDays ?? c.joined_days ?? 30,
        lastActiveDays: c.lastActiveDays ?? c.last_active_days ?? 1,
      }));
      return liveCustomersCache;
    }
  } catch (err) {
    console.warn("Notice: Fetching customers from DB failed, using local cache:", err);
  }
  return customers;
}

export function findCustomer(id: string): Customer | undefined {
  return liveCustomersCache.find((c) => c.id === id) || customers.find((c) => c.id === id);
}
