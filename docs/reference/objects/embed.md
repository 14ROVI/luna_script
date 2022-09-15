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
- [`set_title`](#settitletitle-string)
- `set_description`
- `set_timestamp`
- `set_colour`
- `set_footer`
- `set_image_url`
- `set_thumbnail_url`
- `set_author`
- `add_field`

#### `set_title(title: String)`
Sets the title of the embed.


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