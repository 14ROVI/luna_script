# Embed

Represents a discord rich embed. Each function that edits the embed also returns the new embed to allow for modern fluent styling.

### Attributes
| Name | Type |
| --- | --- |
| `author` | [`EmbedAuthor`](#embedauthor) |
| `colour` | [`Number`](number.md) |
| `title` | [`String`](string.md) |
| `description` | [`String`](string.md) |
| `fields` | [`EmbedField`](#embedfield) |
| `footer` | [`EmbedFooter`](#embedfooter) |
| `image_url` | [`String`](string.md) |
| `thumbnail_url` | [`String`](string.md) |
| `timestamp` | [`Number`](string.md) |

### Functions
- [`set_title`](#set_titletitle-string)
- [`set_description`](#set_descriptiondescription-string)
- [`set_timestamp`](#set_timestamptimestamp-number)
- [`set_colour`](#set_colourcolour-number)
- [`set_footer`](#set_footertext-string-icon_url-string)
- [`set_image_url`](#set_image_urlurl-string)
- [`set_thumbnail_url`](#set_thumbnail_urlurl-string)
- [`set_author`](#set_authorname-string-url-string-icon_url-string)
- [`add_field`](#add_fieldname-string-value-string-inline-number)

#### `set_title(title: String)`
Sets the title of the embed.
#### `set_description(description: String)`
Sets the description of the embed.
#### `set_timestamp(timestamp: Number)`
Sets the timestamp of the embed. Takes in an unix epoch in seconds format.
#### `set_colour(colour: Number)`
Sets the accent colour of the embed. Takes in the colour in rgb format as a number. 0 is black, 16777216 is white.
#### `set_footer(text: String, icon_url: String)`
Sets the footer of the embed. If you want no text or icon_url set them as null.
#### `set_image_url(url: String)`
Sets the image url of the embed.
#### `set_thumbnail_url(url: String)`
Sets the thumbnail url of the embed.
#### `set_author(name: String, url: String, icon_url: String)`
Sets the author of the embed. If you want something to be missing, set them as null.
#### `add_field(name: String, value: String, inline: Number)`
Adds a field to the embed. Inline must be true or false (1 or 0).


# EmbedAuthor

Represents the author data of an embed.

### Attributes
| Name | Type |
| --- | --- |
| `name` | [`String`](string.md) |
| `url` | [`String`](string.md) |
| `icon_url` | [`String`](string.md) |


# EmbedField

Represents a field of an embed.

### Attributes
| Name | Type |
| --- | --- |
| `name` | [`String`](string.md) |
| `value` | [`String`](string.md) |
| `inline` | [`Number`](number.md) |

`inline` is either true or false (1 or 0)


# EmbedFooter

Represents the footer data of an embed.

### Attributes
| Name | Type |
| --- | --- |
| `text` | [`String`](string.md) |
| `icon_url` | [`String`](string.md) |
