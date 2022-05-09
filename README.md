# Luna script
The programming language for https://luna.rovi.me custom commands
> There will be full documentation in the future and at the moment it is quite simple.

## Examples

#### Competition submission
```py
var submission_channel = guild.get_channel(649188237854402159)
submission_channel.send(invoker.mention + " has submitted this video: " + video_url)
interaction.respond("Your submission has been recorded!")
```
#### Sending an embed
```py
var embed = Embed()
embed.set_title("This is an example")
embed.set_description("On how to use embeds in this language")
var embed = embed.set_footer("You can use fluent stylying", Number.null)
# Comments work too btw!
# Number.null is used for telling it you don't want anything there (in this case the footer's icon_url)
interaction.respond(embed.add_field("sending?", "It's that easy 😌"))
```
