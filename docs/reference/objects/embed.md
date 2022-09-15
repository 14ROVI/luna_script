# Embed

Represents a discord rich embed.

### Functions
- `set_title`
- `set_description`
- `set_timestamp`
- `set_colour`
- `set_footer`
- `set_image_url`
- `set_thumbnail_url`
- `set_author`
- `add_field`

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



# EmbedAuthor

Represents the author data of an embed.

### Attributes
- `name`
- `url`
- `icon_url`


# EmbedField

Represents a field of an embed.

### Attributes
- `name`
- `value`
- `inline`



# EmbedFooter

Represents the footer data of an embed.

### Attributes
- `text`
- `icon_url`