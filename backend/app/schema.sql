-- Enable UUID generation (if not already enabled)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Customer table
CREATE TABLE customer (
    customer_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    preferred_language VARCHAR(2),
    communication_method VARCHAR(20),
    sentiment_score FLOAT,
    customer_type VARCHAR(20),
    mailing_address TEXT
);

-- Agent table
CREATE TABLE agent (
    agent_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    contact_info TEXT,
    agency_affiliation TEXT,
    license_status VARCHAR(20),
    commission_rate NUMERIC(5,2)
);

-- Policy table
CREATE TABLE policy (
    policy_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    policy_number VARCHAR(50) UNIQUE NOT NULL,
    customer_id UUID NOT NULL REFERENCES customer(customer_id),
    policy_type VARCHAR(10),
    status VARCHAR(20),
    effective_date DATE,
    expiration_date DATE,
    renewal_date DATE,
    underwriting_company TEXT,
    agent_id UUID REFERENCES agent(agent_id),
    term_length_months INTEGER
);

-- BillingAccount table (one-to-one with policy)
CREATE TABLE billing_account (
    billing_account_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    policy_id UUID NOT NULL UNIQUE REFERENCES policy(policy_id),
    billing_plan VARCHAR(20),
    current_balance NUMERIC(12,2),
    next_due_date DATE,
    escrow_indicator BOOLEAN,
    payment_method VARCHAR(20),
    autopay_enabled BOOLEAN,
    lender_billed BOOLEAN
);

-- Property table (one-to-one with policy)
CREATE TABLE property (
    property_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    policy_id UUID NOT NULL UNIQUE REFERENCES policy(policy_id),
    address TEXT,
    occupancy_type VARCHAR(20),
    dwelling_type VARCHAR(50),
    year_built INTEGER,
    roof_type VARCHAR(50),
    roof_age INTEGER,
    construction_type VARCHAR(50),
    square_footage INTEGER,
    stories INTEGER,
    protection_class VARCHAR(10)
);

-- Coverage table (many-to-one to policy)
CREATE TABLE coverage (
    coverage_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    policy_id UUID NOT NULL REFERENCES policy(policy_id),
    coverage_type CHAR(1),
    limit_amount NUMERIC(12,2),
    deductible_type VARCHAR(50),
    deductible_amount NUMERIC(12,2),
    endorsements JSONB,
    discounts JSONB,
    surcharges JSONB,
    replacement_cost NUMERIC(12,2)
);

-- Claim table (many-to-one to policy)
CREATE TABLE claim (
    claim_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    policy_id UUID NOT NULL REFERENCES policy(policy_id),
    claim_date DATE,
    claim_type VARCHAR(20),
    amount_paid NUMERIC(12,2),
    adjuster_contact TEXT
);

-- Cancellation table (zero-or-one per policy)
CREATE TABLE cancellation (
    cancellation_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    policy_id UUID UNIQUE REFERENCES policy(policy_id),
    cancellation_date DATE,
    reason TEXT,
    reinstatement_status VARCHAR(20),
    reinstatement_fee NUMERIC(12,2),
    grace_period_days INTEGER
);

-- Payment table (many-to-one to billing_account)
CREATE TABLE payment (
    payment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    billing_account_id UUID NOT NULL REFERENCES billing_account(billing_account_id),
    payment_date DATE,
    amount_paid NUMERIC(12,2),
    payment_status VARCHAR(20),
    refund_issued BOOLEAN,
    nsf_flag BOOLEAN
);

-- ChatInteraction table
CREATE TABLE chat_interaction (
    chat_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID NOT NULL REFERENCES customer(customer_id),
    occurred_at TIMESTAMPTZ DEFAULT now(),
    intent_classification VARCHAR(50),
    ai_confidence_score FLOAT,
    resolved BOOLEAN,
    escalation_flag BOOLEAN,
    chat_notes TEXT
);

-- AI_Metadata table (one-to-one with chat_interaction)
CREATE TABLE ai_metadata (
    metadata_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chat_id UUID NOT NULL UNIQUE REFERENCES chat_interaction(chat_id),
    matched_faq_id VARCHAR(100),
    kb_article_link TEXT,
    improvement_feedback TEXT,
    user_authenticated BOOLEAN,
    last_sync_time TIMESTAMPTZ
);
