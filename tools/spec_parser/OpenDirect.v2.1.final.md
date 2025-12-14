# OpenDirect 2.1 Specification

## Object: Organization

Organizations are top-level entities representing publishers, buyers, agencies, or ad networks.

|Attribute|Description|Type|
|--|--|--|
|id*|Unique identifier for the organization|string (36)|
|name*|Organization display name|string (255)|
|address|Physical address of the organization|Address object|
|contacts|List of contact persons|Contact[] array|
|disapprovalReasons|Reasons for disapproval if applicable|string array|
|status*|Current status of the organization|enum (Active, Inactive, Pending, Disapproved)|
|url|Organization website URL|string (1024)|
|phone|Primary phone number|string (50)|
|fax|Fax number|string (50)|
|ext|Custom extension object|object|

## Object: Account

Accounts represent buyers or advertisers under an organization.

|Attribute|Description|Type|
|--|--|--|
|id*|Unique identifier for the account|string (36)|
|buyerId*|Reference to the buyer organization ID|string (36)|
|advertiserId|Reference to the advertiser organization ID|string (36)|
|name*|Account display name|string (255)|
|providerData|Provider-specific data|string|
|status*|Current status of the account|enum (Active, Inactive, Pending, Disapproved)|
|ext|Custom extension object|object|

## Object: Order

Orders contain one or more lines representing advertising campaigns.

|Attribute|Description|Type|
|--|--|--|
|id*|Unique identifier for the order|string (36)|
|accountId*|Reference to the account ID|string (36)|
|name*|Order display name|string (255)|
|brand|Brand being advertised|AdvertiserBrand object|
|budget|Total budget for the order|number|
|currency|Currency code (ISO 4217)|string (3)|
|startDate*|Campaign start date|date-time|
|endDate|Campaign end date|date-time|
|providerData|Provider-specific data|string|
|status*|Current status of the order|enum (Draft, Pending, Approved, Rejected, InFlight, Stopped, Expired, Completed)|
|orderExpiryDate|Date when order expires if not approved|date-time|
|preferredBillingMethod|Preferred billing method|enum (Electronic, Postal)|
|contacts|List of contact persons|Contact[] array|
|ext|Custom extension object|object|

## Object: Line

Lines represent individual line items within an order.

|Attribute|Description|Type|
|--|--|--|
|id*|Unique identifier for the line|string (36)|
|orderId*|Reference to the parent order ID|string (36)|
|name*|Line display name|string (255)|
|productId|Reference to the product being purchased|string (36)|
|bookingStatus*|Booking status of the line|enum (Draft, PendingReservation, Reserved, PendingBooking, Booked, InFlight, Finished, Stopped, Cancelled, Expired, Declined, ChangePending)|
|startDate*|Line start date|date-time|
|endDate|Line end date|date-time|
|rate|Rate for the line|number|
|rateType*|Type of rate|enum (CPM, CPC, CPA, CPD, FlatRate)|
|quantity|Quantity to purchase|integer|
|cost|Total cost of the line|number|
|comment|Comments or notes|string|
|frequencyCount|Frequency cap count|integer|
|frequencyInterval|Frequency cap interval|enum (Day, Week, Month, NotApplicable)|
|targeting|Targeting specifications|Segment[] array|
|providerData|Provider-specific data|string|
|ext|Custom extension object|object|

## Object: Creative

Creatives represent advertising creative assets.

|Attribute|Description|Type|
|--|--|--|
|id*|Unique identifier for the creative|string (36)|
|accountId*|Reference to the account ID|string (36)|
|name*|Creative display name|string (255)|
|adFormatType*|Type of creative format|enum (Display, Video, Audio, Native)|
|adomain|Advertiser domain for verification|string array|
|adQualityStatus|Ad quality review status|enum (Approved, Pending, Disapproved)|
|adQualityProvider|Ad quality review provider name|string|
|creativeApprovals|List of creative approvals|CreativeApproval[] array|
|geometry|Creative dimensions (WxH)|string|
|language|Language of the creative|string|
|secureUrl|HTTPS URL of the creative|string|
|maturityLevel|Maturity/content rating|enum (General, Mature, Everyone, Teen)|
|providerData|Provider-specific data|string|
|ext|Custom extension object|object|

## Object: Assignment

Assignments link creatives to lines.

|Attribute|Description|Type|
|--|--|--|
|id*|Unique identifier for the assignment|string (36)|
|lineId*|Reference to the line ID|string (36)|
|creativeId*|Reference to the creative ID|string (36)|
|status*|Current status of the assignment|enum (Active, Inactive)|
|weight|Weight for creative rotation|integer|
|startDate|Assignment start date|date-time|
|endDate|Assignment end date|date-time|
|ext|Custom extension object|object|

## Object: Product

Products define inventory available for purchase.

|Attribute|Description|Type|
|--|--|--|
|id*|Unique identifier for the product|string (36)|
|publisherId*|Reference to the publisher organization ID|string (36)|
|name*|Product display name|string (255)|
|description|Product description|string (3000)|
|productType|Type of product|string|
|rateType*|Type of rate|enum (CPM, CPC, CPA, CPD, FlatRate)|
|basePrice|Base price for the product|number|
|currency|Currency code (ISO 4217)|string (3)|
|deliveryType|Type of delivery|enum (Exclusive, Guaranteed, NonGuaranteed)|
|domain|Domain where ads will appear|string|
|url|URL of the product page|string|
|geometry|Ad dimensions available|string array|
|minSpend|Minimum spend required|number|
|language|Languages supported|string array|
|targetedSegments|Available targeting segments|Segment[] array|
|icon|Icon URL for the product|string|
|adUnitIds|List of ad unit IDs|string array|
|ext|Custom extension object|object|

## Object: Contact

Contact information for organization representatives.

|Attribute|Description|Type|
|--|--|--|
|id|Unique identifier for the contact|string (36)|
|email*|Email address|string (255)|
|honorific|Title or honorific (Mr., Ms., Dr.)|string (20)|
|firstName*|First name|string (100)|
|lastName*|Last name|string (100)|
|title|Job title|string (100)|
|phone|Phone number|string (50)|
|fax|Fax number|string (50)|
|address|Physical address|Address object|
|type*|Type of contact|enum (Billing, Buyer, Creative, Sales, Technical)|
|ext|Custom extension object|object|

## Object: AdvertiserBrand

Brand information for the advertiser.

|Attribute|Description|Type|
|--|--|--|
|id*|Unique identifier for the brand|string (36)|
|organizationId|Reference to organization ID|string (36)|
|name*|Brand name|string (255)|
|domain|Brand domain|string (255)|
|category|IAB category code|string (100)|
|ext|Custom extension object|object|

## Object: Address

Physical address information.

|Attribute|Description|Type|
|--|--|--|
|street1*|Primary street address|string (255)|
|street2|Secondary street address|string (255)|
|city*|City name|string (100)|
|state|State or province|string (50)|
|postalCode|Postal or ZIP code|string (20)|
|country*|Country code (ISO 3166-1 alpha-2)|string (2)|
|ext|Custom extension object|object|

## Object: AdUnit

Ad units represent placement locations for ads.

|Attribute|Description|Type|
|--|--|--|
|id*|Unique identifier for the ad unit|string (36)|
|publisherId*|Reference to publisher organization ID|string (36)|
|name*|Ad unit display name|string (255)|
|geometry*|Dimensions (WxH)|string (50)|
|adFormatType*|Type of ad format|enum (Display, Video, Audio, Native)|
|path|URL path where ad unit appears|string (1024)|
|domain|Domain where ad unit appears|string (255)|
|position|Position on page|enum (AboveFold, BelowFold, Header, Footer, Sidebar, Fullscreen)|
|ext|Custom extension object|object|

## Object: ChangeRequest

Change requests for modifying existing entities.

|Attribute|Description|Type|
|--|--|--|
|id*|Unique identifier for the change request|string (36)|
|entityType*|Type of entity being changed|enum (Order, Line, Creative, Assignment)|
|entityId*|ID of entity being changed|string (36)|
|accountId*|Reference to account ID|string (36)|
|status*|Status of the change request|enum (Pending, Approved, Rejected, Cancelled)|
|requestedBy|User who requested the change|string (255)|
|requestedDate*|Date the change was requested|date-time|
|reviewedBy|User who reviewed the change|string (255)|
|reviewedDate|Date the change was reviewed|date-time|
|comment|Comments about the change|string (3000)|
|changes|JSON object describing the changes|object|
|ext|Custom extension object|object|

## Object: Message

Messages for communication between parties.

|Attribute|Description|Type|
|--|--|--|
|id*|Unique identifier for the message|string (36)|
|entityType|Type of entity the message relates to|enum (Order, Line, Creative, Assignment, Account)|
|entityId|ID of related entity|string (36)|
|from*|Sender email or identifier|string (255)|
|to|Recipient email or identifier|string (255)|
|subject|Message subject|string (500)|
|body*|Message body content|string (10000)|
|timestamp*|When the message was sent|date-time|
|read|Whether message has been read|boolean|
|ext|Custom extension object|object|

## Object: Placement

Placements define where ads will be shown.

|Attribute|Description|Type|
|--|--|--|
|id*|Unique identifier for the placement|string (36)|
|publisherId*|Reference to publisher organization ID|string (36)|
|name*|Placement display name|string (255)|
|description|Placement description|string (3000)|
|adUnitIds|List of ad unit IDs in this placement|string array|
|siteId|Reference to site ID|string (36)|
|tagId|Ad tag identifier|string (255)|
|url|URL where placement appears|string (1024)|
|status|Status of the placement|enum (Active, Inactive, Archived)|
|ext|Custom extension object|object|

## Object: CustomProperty

Custom properties for extending objects.

|Attribute|Description|Type|
|--|--|--|
|name*|Property name|string (100)|
|value*|Property value|string (1000)|
|type|Data type of the property|enum (String, Integer, Number, Boolean, Date)|
|ext|Custom extension object|object|

## Object: Segment

Targeting segments for audience selection.

|Attribute|Description|Type|
|--|--|--|
|id*|Unique identifier for the segment|string (36)|
|name*|Segment display name|string (255)|
|description|Segment description|string (1000)|
|type*|Type of targeting|enum (Age, Gender, Geography, Behavioral, Contextual, Device, Daypart, Technology)|
|value|Targeting value or criteria|string (500)|
|operator|Comparison operator|enum (Equals, NotEquals, GreaterThan, LessThan, Contains, In)|
|ext|Custom extension object|object|

## Object: CreativeApproval

Approval status for creative reviews.

|Attribute|Description|Type|
|--|--|--|
|id*|Unique identifier for the approval|string (36)|
|creativeId*|Reference to creative ID|string (36)|
|publisherId|Reference to publisher organization ID|string (36)|
|status*|Approval status|enum (Approved, Pending, Rejected)|
|reviewedBy|User who reviewed|string (255)|
|reviewedDate|Date of review|date-time|
|reason|Reason for rejection if applicable|string (1000)|
|ext|Custom extension object|object|

## Object: Stats

Statistics and performance metrics.

|Attribute|Description|Type|
|--|--|--|
|entityType*|Type of entity|enum (Order, Line, Creative)|
|entityId*|ID of entity|string (36)|
|date*|Date of the stats|date|
|impressions|Number of impressions|integer|
|clicks|Number of clicks|integer|
|conversions|Number of conversions|integer|
|spend|Amount spent|number|
|revenue|Revenue generated|number|
|ctr|Click-through rate|number|
|conversionRate|Conversion rate|number|
|ext|Custom extension object|object|

## Object: Site

Sites represent publisher properties.

|Attribute|Description|Type|
|--|--|--|
|id*|Unique identifier for the site|string (36)|
|publisherId*|Reference to publisher organization ID|string (36)|
|name*|Site display name|string (255)|
|domain*|Site domain|string (255)|
|url|Site URL|string (1024)|
|category|IAB category codes|string array|
|language|Languages supported|string array|
|description|Site description|string (3000)|
|status|Status of the site|enum (Active, Inactive, UnderReview)|
|ext|Custom extension object|object|

## Object: Deal

Private marketplace deals and packages.

|Attribute|Description|Type|
|--|--|--|
|id*|Unique identifier for the deal|string (36)|
|publisherId*|Reference to publisher organization ID|string (36)|
|buyerId*|Reference to buyer organization ID|string (36)|
|name*|Deal display name|string (255)|
|dealType*|Type of deal|enum (ProgrammaticGuaranteed, PreferredDeal, PrivateAuction)|
|startDate*|Deal start date|date-time|
|endDate|Deal end date|date-time|
|floorPrice|Minimum price|number|
|currency|Currency code|string (3)|
|impressions|Number of impressions available|integer|
|productIds|List of product IDs in the deal|string array|
|status*|Status of the deal|enum (Draft, Pending, Active, Expired, Cancelled)|
|ext|Custom extension object|object|

## Object: Report

Reporting and analytics data.

|Attribute|Description|Type|
|--|--|--|
|id*|Unique identifier for the report|string (36)|
|name*|Report display name|string (255)|
|reportType*|Type of report|enum (Performance, Delivery, Billing, Inventory)|
|entityType|Type of entity being reported on|enum (Order, Line, Creative, Product, Account)|
|entityId|ID of entity being reported on|string (36)|
|startDate*|Report period start date|date-time|
|endDate*|Report period end date|date-time|
|format|Report format|enum (CSV, JSON, XML, PDF)|
|status|Status of report generation|enum (Pending, Processing, Complete, Failed)|
|url|URL to download the report|string (1024)|
|generatedDate|Date the report was generated|date-time|
|ext|Custom extension object|object|
