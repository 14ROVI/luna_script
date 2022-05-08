# luna_script
The programming language for https://luna.rovi.me custom commands
> There will be full documentation in the future and at the moment it is quite simple.

## Examples

#### Competition submission
```py
var submission_channel = guild.get_channel(649188237854402159)
submission_channel.send(invoker.mention + " has submitted this video: " + video_url)
interaction.respond("Your submission has been recorded!")
```
