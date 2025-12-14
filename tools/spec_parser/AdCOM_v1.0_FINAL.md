# AdCOM v1.0 Specification

## Overview

AdCOM (Advertising Common Object Model) provides a common language for communication between buyers, sellers, and intermediaries in the digital advertising supply chain. This specification defines the objects and structures for representing ads, creative assets, and context information.

---

## Object: Ad

The Ad object represents a single advertisement unit.

| Attribute | Description | Type |
|-----------|-------------|------|
| id* | Unique identifier for the ad | string |
| adomain | Advertiser domains | array of strings |
| bundle | Application bundle/package name | string |
| iurl | Image URL for content review | string |
| cat | IAB content categories | array of strings |
| cattax | Taxonomy used for categories | integer |
| lang | Language using ISO-639-1-alpha-2 | string |
| secure | Flag to indicate if creative is secure | integer |
| init | Initial date/time of availability | string |
| lastmod | Date/time of last modification | string |
| display | Display ad object | Display object |
| video | Video ad object | Video object |
| audio | Audio ad object | Audio object |
| ext | Extension object | object |

---

## Object: Display

Object representing display advertisement creative.

| Attribute | Description | Type |
|-----------|-------------|------|
| mime* | MIME type of creative | string |
| api | List of supported API frameworks | array of integers |
| type | Type of display creative | integer |
| w | Width in pixels or % | integer |
| h | Height in pixels or % | integer |
| wratio | Width ratio for responsive ads | integer |
| hratio | Height ratio for responsive ads | integer |
| priv | Privacy policy link | string |
| adm | Ad markup | string |
| curl | Creative URL | string |
| banner | Banner object for simple display ads | Banner object |
| native | Native object for native ads | Native object |
| event | Event trackers | array of Event objects |
| ext | Extension object | object |

---

## Object: Banner

Simple banner object for static or animated creative.

| Attribute | Description | Type |
|-----------|-------------|------|
| img* | Image resource URL | string |
| link | Destination link object | LinkAsset object |
| w | Width in pixels | integer |
| h | Height in pixels | integer |
| alt | Alternative text | string |
| ext | Extension object | object |

---

## Object: Video

Video advertisement object.

| Attribute | Description | Type |
|-----------|-------------|------|
| mime* | MIME types of video | array of strings |
| api | List of supported API frameworks | array of integers |
| type | Type of video ad | integer |
| w | Width in pixels | integer |
| h | Height in pixels | integer |
| skip | Video can be skipped | integer |
| skipmin | Minimum duration before skip | integer |
| skipafter | Skip button shown after duration | integer |
| playmethod | Playback methods | array of integers |
| playend | End of playback action | integer |
| clktype | Click behavior type | integer |
| maxdur | Maximum duration in seconds | integer |
| mindur | Minimum duration in seconds | integer |
| ext | Extension object | object |

---

## Object: Audio

Audio advertisement object.

| Attribute | Description | Type |
|-----------|-------------|------|
| mime* | MIME types of audio | array of strings |
| api | List of supported API frameworks | array of integers |
| type | Type of audio ad | integer |
| maxdur | Maximum duration in seconds | integer |
| mindur | Minimum duration in seconds | integer |
| feed | Type of audio feed | integer |
| nvol | Volume normalization mode | integer |
| ext | Extension object | object |

---

## Object: Native

Native advertisement object containing multiple assets.

| Attribute | Description | Type |
|-----------|-------------|------|
| priv | Privacy policy URL | string |
| link* | Destination link object | LinkAsset object |
| asset* | Array of asset objects | array of Asset objects |
| event | Event trackers | array of Event objects |
| ext | Extension object | object |

---

## Object: Asset

Asset object for native ads.

| Attribute | Description | Type |
|-----------|-------------|------|
| id | Asset ID | integer |
| req | Asset is required | integer |
| title | Title asset | TitleAsset object |
| img | Image asset | ImageAsset object |
| video | Video asset | VideoAsset object |
| data | Data asset | DataAsset object |
| link | Link asset | LinkAsset object |
| ext | Extension object | object |

---

## Object: LinkAsset

Link asset for clickthrough and tracking.

| Attribute | Description | Type |
|-----------|-------------|------|
| url* | Landing URL | string |
| urlfb | Fallback URL | string |
| trkr | Tracking URLs | array of strings |
| ext | Extension object | object |

---

## Object: ImageAsset

Image asset for native ads.

| Attribute | Description | Type |
|-----------|-------------|------|
| url* | Image URL | string |
| w | Width in pixels | integer |
| h | Height in pixels | integer |
| type | Image type | integer |
| ext | Extension object | object |

---

## Object: VideoAsset

Video asset for native ads.

| Attribute | Description | Type |
|-----------|-------------|------|
| adm | Video markup | string |
| curl | Video creative URL | string |
| ext | Extension object | object |

---

## Object: TitleAsset

Title asset for native ads.

| Attribute | Description | Type |
|-----------|-------------|------|
| text* | Title text | string |
| len | Maximum length | integer |
| ext | Extension object | object |

---

## Object: DataAsset

Structured data asset for native ads.

| Attribute | Description | Type |
|-----------|-------------|------|
| value* | Data value | string |
| len | Maximum length | integer |
| type | Data asset type | integer |
| ext | Extension object | object |

---

## Object: Event

Event tracking object for impressions and user interactions.

| Attribute | Description | Type |
|-----------|-------------|------|
| type* | Event type | integer |
| method* | Event tracking method | integer |
| api | API frameworks | array of integers |
| url | Tracking URL | string |
| cdata | Custom data | object |
| ext | Extension object | object |

---

## Object: Publisher

Publisher of content.

| Attribute | Description | Type |
|-----------|-------------|------|
| id | Publisher ID | string |
| name | Publisher name | string |
| domain | Publisher domain | string |
| cat | IAB content categories | array of strings |
| cattax | Category taxonomy | integer |
| ext | Extension object | object |

---

## Object: Content

Details about the content.

| Attribute | Description | Type |
|-----------|-------------|------|
| id | Content ID | string |
| title | Content title | string |
| series | Content series | string |
| season | Content season | string |
| episode | Episode number | integer |
| artist | Artist name | string |
| genre | Content genre | string |
| album | Album name | string |
| isrc | International Standard Recording Code | string |
| url | Content URL | string |
| cat | IAB content categories | array of strings |
| cattax | Category taxonomy | integer |
| prodq | Production quality | integer |
| context | Content context | integer |
| rating | Content rating | string |
| urating | User rating | string |
| mrating | Media rating | integer |
| keywords | Content keywords | string |
| live | Live content flag | integer |
| len | Content length in seconds | integer |
| lang | Language code | string |
| embed | Content is embedded | integer |
| producer | Content producer | Publisher object |
| ext | Extension object | object |

---

## Object: User

User or audience information.

| Attribute | Description | Type |
|-----------|-------------|------|
| id | User ID | string |
| buyeruid | Buyer's user ID | string |
| yob | Year of birth | integer |
| gender | Gender (M/F/O) | string |
| keywords | User interests | string |
| consent | GDPR consent string | string |
| geo | User geographic location | Geo object |
| ext | Extension object | object |

---

## Object: Device

Device information.

| Attribute | Description | Type |
|-----------|-------------|------|
| type | Device type | integer |
| ua | User agent string | string |
| ifa | ID for advertisers | string |
| dnt | Do not track flag | integer |
| lmt | Limit ad tracking flag | integer |
| make | Device make | string |
| model | Device model | string |
| os | Operating system | string |
| osv | OS version | string |
| h | Screen height in pixels | integer |
| w | Screen width in pixels | integer |
| ppi | Screen pixels per inch | integer |
| pxratio | Pixel ratio | float |
| js | JavaScript support | integer |
| lang | Browser language | string |
| ip | IPv4 address | string |
| ipv6 | IPv6 address | string |
| xff | X-Forwarded-For header | string |
| geo | Device geographic location | Geo object |
| ext | Extension object | object |

---

## Object: Geo

Geographic location information.

| Attribute | Description | Type |
|-----------|-------------|------|
| type | Source of location data | integer |
| lat | Latitude | float |
| lon | Longitude | float |
| accur | Accuracy in meters | integer |
| lastfix | Timestamp of last fix | integer |
| ipserv | IP geolocation service | integer |
| country | Country code (ISO-3166-1 Alpha-3) | string |
| region | Region code (ISO-3166-2) | string |
| metro | Metropolitan code | string |
| city | City name | string |
| zip | Zip/postal code | string |
| utcoffset | Local time offset from UTC | integer |
| ext | Extension object | object |

---

## Enums and Lists

### List: API Frameworks

API frameworks supported by creative or placement.

| Value | Description |
|-------|-------------|
| 1 | VPAID 1.0 |
| 2 | VPAID 2.0 |
| 3 | MRAID-1 |
| 4 | ORMMA |
| 5 | MRAID-2 |
| 6 | MRAID-3 |
| 7 | OMID-1 |

### List: Creative Subtypes

Subtype of display creative.

| Value | Description |
|-------|-------------|
| 1 | HTML |
| 2 | AMPHTML |
| 3 | Structured Image |
| 4 | Structured Native |

### List: Production Quality

Production quality of content.

| Value | Description |
|-------|-------------|
| 0 | Unknown |
| 1 | Professionally Produced |
| 2 | Prosumer |
| 3 | User Generated |

### List: Size Units

Units of measurement for sizes.

| Value | Description |
|-------|-------------|
| 1 | Device Independent Pixels |
| 2 | Inches |
| 3 | Centimeters |

### List: Pod Sequence

Video pod sequence options.

| Value | Description |
|-------|-------------|
| -1 | Last |
| 0 | Any |
| 1 | First |

### List: Volume Normalization Modes

Volume normalization mode for audio.

| Value | Description |
|-------|-------------|
| 0 | None |
| 1 | Average Volume |
| 2 | Peak Volume |
| 3 | Loudness |
| 4 | Custom |

### List: Event Types

Event types for tracking.

| Value | Description |
|-------|-------------|
| 1 | Impression |
| 2 | ViewableMRC50 |
| 3 | ViewableMRC100 |
| 4 | ViewableVideo50 |

### List: Event Methods

Methods for event tracking.

| Value | Description |
|-------|-------------|
| 1 | Image-Pixel |
| 2 | JavaScript |

### List: Device Types

Device type classifications.

| Value | Description |
|-------|-------------|
| 1 | Mobile/Tablet |
| 2 | Personal Computer |
| 3 | Connected TV |
| 4 | Phone |
| 5 | Tablet |
| 6 | Connected Device |
| 7 | Set Top Box |

---

## Extension Object

Throughout the specification, objects may include an `ext` field allowing for custom extensions. The structure of extension objects is implementation-specific.

---

**Copyright © 2018 IAB Technology Laboratory**
