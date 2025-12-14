"""Tests for generated Adcom Pydantic models."""

import pytest
from pydantic import ValidationError

from opendirect21.models.generated.adcom import (
    # Media objects
    Ad,
    Display,
    Banner,
    Video,
    Audio,
    Native,
    # Asset objects
    Asset,
    LinkAsset,
    ImageAsset,
    VideoAsset,
    TitleAsset,
    DataAsset,
    Event,
    # Context objects
    Publisher,
    Content,
    User,
    Device,
    Geo,
    # Enums
    APIFrameworks,
    CreativeSubtypes,
    ProductionQuality,
    SizeUnits,
    PodSequence,
    VolumeNormalizationModes,
    EventTypes,
    EventMethods,
    DeviceTypes,
)


def test_ad_model_creation():
    """Test creating Ad model instance."""
    ad = Ad(id="ad-123", adomain=["example.com"], secure=1)

    assert ad.id == "ad-123"
    assert ad.adomain == ["example.com"]
    assert ad.secure == 1
    assert ad.bundle is None


def test_ad_model_required_fields():
    """Test Ad model required field validation."""
    # id is required
    with pytest.raises(ValidationError):
        Ad()


def test_display_model_creation():
    """Test creating Display model instance."""
    display = Display(
        mime="text/html",
        w=300,
        h=250,
        api=[1, 2],
        type=1,
    )

    assert display.mime == "text/html"
    assert display.w == 300
    assert display.h == 250
    assert display.api == [1, 2]


def test_banner_model_creation():
    """Test creating Banner model instance."""
    banner = Banner(img="https://example.com/banner.jpg", w=728, h=90)

    assert banner.img == "https://example.com/banner.jpg"
    assert banner.w == 728
    assert banner.h == 90


def test_video_model_creation():
    """Test creating Video model instance."""
    video = Video(
        mime=["video/mp4", "video/webm"],
        w=640,
        h=480,
        maxdur=30,
        mindur=10,
    )

    assert video.mime == ["video/mp4", "video/webm"]
    assert video.w == 640
    assert video.maxdur == 30


def test_audio_model_creation():
    """Test creating Audio model instance."""
    audio = Audio(mime=["audio/mp3", "audio/aac"], maxdur=30, mindur=5)

    assert audio.mime == ["audio/mp3", "audio/aac"]
    assert audio.maxdur == 30


def test_native_model_creation():
    """Test creating Native model instance."""
    link = LinkAsset(url="https://example.com")
    asset = Asset(id=1, req=1, title=TitleAsset(text="Test Title"))

    native = Native(link=link, asset=[asset])

    assert native.link.url == "https://example.com"
    assert len(native.asset) == 1


def test_asset_models():
    """Test creating various asset models."""
    # LinkAsset
    link = LinkAsset(url="https://example.com", urlfb="https://fallback.com")
    assert link.url == "https://example.com"

    # ImageAsset
    image = ImageAsset(url="https://example.com/image.jpg", w=300, h=250)
    assert image.url == "https://example.com/image.jpg"

    # TitleAsset
    title = TitleAsset(text="Test Title", len=50)
    assert title.text == "Test Title"

    # DataAsset
    data = DataAsset(value="Test Data", type=1)
    assert data.value == "Test Data"


def test_event_model_creation():
    """Test creating Event model instance."""
    event = Event(type=1, method=1, url="https://example.com/track")

    assert event.type == 1
    assert event.method == 1
    assert event.url == "https://example.com/track"


def test_publisher_model_creation():
    """Test creating Publisher model instance."""
    publisher = Publisher(
        id="pub-123", name="Test Publisher", domain="publisher.com"
    )

    assert publisher.id == "pub-123"
    assert publisher.name == "Test Publisher"


def test_content_model_creation():
    """Test creating Content model instance."""
    content = Content(
        id="content-123",
        title="Test Video",
        url="https://example.com/video",
        len=300,
    )

    assert content.id == "content-123"
    assert content.title == "Test Video"
    assert content.len == 300


def test_user_model_creation():
    """Test creating User model instance."""
    user = User(id="user-123", yob=1990, gender="M")

    assert user.id == "user-123"
    assert user.yob == 1990
    assert user.gender == "M"


def test_device_model_creation():
    """Test creating Device model instance."""
    device = Device(
        type=1,
        ua="Mozilla/5.0...",
        ip="192.168.1.1",
        make="Apple",
        model="iPhone",
        os="iOS",
    )

    assert device.type == 1
    assert device.make == "Apple"
    assert device.model == "iPhone"


def test_geo_model_creation():
    """Test creating Geo model instance."""
    geo = Geo(
        lat=37.7749,
        lon=-122.4194,
        country="USA",
        city="San Francisco",
    )

    assert geo.lat == 37.7749
    assert geo.lon == -122.4194
    assert geo.city == "San Francisco"


def test_nested_objects():
    """Test creating nested object structures."""
    # Create a complete ad with nested objects
    geo = Geo(lat=37.7749, lon=-122.4194, country="USA")
    device = Device(type=4, make="Apple", model="iPhone", geo=geo)
    user = User(id="user-123", geo=geo)

    publisher = Publisher(id="pub-123", name="Test Publisher")
    content = Content(
        id="content-123",
        title="Test Content",
        producer=publisher,
    )

    display = Display(
        mime="text/html",
        w=300,
        h=250,
        banner=Banner(img="https://example.com/banner.jpg"),
    )

    ad = Ad(
        id="ad-123",
        adomain=["example.com"],
        display=display,
    )

    assert ad.display.banner.img == "https://example.com/banner.jpg"
    assert device.geo.country == "USA"


def test_api_frameworks_enum():
    """Test APIFrameworks enum."""
    assert APIFrameworks.VALUE_1.value == "1"
    assert APIFrameworks.VALUE_7.value == "7"

    # Enum has expected number of values
    assert len(APIFrameworks) == 7


def test_creative_subtypes_enum():
    """Test CreativeSubtypes enum."""
    assert CreativeSubtypes.VALUE_1.value == "1"
    assert len(CreativeSubtypes) == 4


def test_device_types_enum():
    """Test DeviceTypes enum."""
    assert DeviceTypes.VALUE_4.value == "4"
    assert len(DeviceTypes) == 7


def test_production_quality_enum():
    """Test ProductionQuality enum."""
    assert ProductionQuality.VALUE_0.value == "0"
    assert len(ProductionQuality) == 4


def test_event_types_enum():
    """Test EventTypes enum."""
    assert EventTypes.VALUE_1.value == "1"
    assert len(EventTypes) == 4


def test_model_extra_fields():
    """Test that models allow extra fields (ConfigDict extra='allow')."""
    # Models should allow extra fields
    ad = Ad(id="ad-123", custom_field="custom_value")

    assert ad.id == "ad-123"
    # Extra field should be allowed
    assert hasattr(ad, "custom_field")


def test_model_dict_conversion():
    """Test converting models to dict."""
    ad = Ad(id="ad-123", adomain=["example.com"], secure=1)

    ad_dict = ad.model_dump()

    assert ad_dict["id"] == "ad-123"
    assert ad_dict["adomain"] == ["example.com"]
    assert ad_dict["secure"] == 1


def test_model_json_serialization():
    """Test JSON serialization of models."""
    ad = Ad(id="ad-123", adomain=["example.com"])

    json_str = ad.model_dump_json()

    assert "ad-123" in json_str
    assert "example.com" in json_str


def test_complex_nested_structure():
    """Test creating a complex nested structure."""
    # Create a native ad with multiple assets
    link = LinkAsset(url="https://example.com")

    title_asset = Asset(id=1, req=1, title=TitleAsset(text="Main Title"))
    image_asset = Asset(id=2, req=1, img=ImageAsset(url="https://example.com/img.jpg"))
    data_asset = Asset(id=3, req=0, data=DataAsset(value="Sponsored", type=1))

    event1 = Event(type=1, method=1, url="https://example.com/impression")
    event2 = Event(type=2, method=2, url="https://example.com/viewable")

    native = Native(
        link=link,
        asset=[title_asset, image_asset, data_asset],
        event=[event1, event2],
    )

    display = Display(mime="text/html", native=native)
    ad = Ad(id="native-ad-123", display=display)

    # Verify structure
    assert ad.display.native.link.url == "https://example.com"
    assert len(ad.display.native.asset) == 3
    assert len(ad.display.native.event) == 2
    assert ad.display.native.asset[0].title.text == "Main Title"


def test_array_field_types():
    """Test that array fields work correctly."""
    ad = Ad(
        id="ad-123",
        adomain=["domain1.com", "domain2.com", "domain3.com"],
        cat=["IAB1", "IAB2"],
    )

    assert len(ad.adomain) == 3
    assert "domain2.com" in ad.adomain
    assert len(ad.cat) == 2


@pytest.mark.parametrize(
    "model_class,required_fields",
    [
        (Ad, {"id"}),
        (Display, {"mime"}),
        (Banner, {"img"}),
        (Video, {"mime"}),
        (Audio, {"mime"}),
        (LinkAsset, {"url"}),
        (ImageAsset, {"url"}),
        (TitleAsset, {"text"}),
        (DataAsset, {"value"}),
        (Event, {"type", "method"}),
    ],
)
def test_model_required_fields(model_class, required_fields):
    """Test that models enforce required fields."""
    # Try to create without required fields - should fail
    with pytest.raises(ValidationError) as exc_info:
        model_class()

    # Check that error mentions required fields
    error_str = str(exc_info.value)
    for field in required_fields:
        assert field in error_str.lower()
