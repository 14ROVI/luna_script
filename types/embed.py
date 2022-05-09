from dis import disco
from discord import Embed as DiscordEmbed
from datetime import datetime

from .. import RTError, RTResult

from . import ClassFunction, Value, String, Number, List


class Embed(Value):
    def __init__(self, value):
        super().__init__()
        self.value: DiscordEmbed = value or DiscordEmbed()
        
        self.symbol_table.set("author", EmbedAuthor(None, None, None))
        self.symbol_table.set("colour", Number.null)
        self.symbol_table.set("title", Number.null)
        self.symbol_table.set("description", Number.null)
        self.symbol_table.set("fields", List([]))
        self.symbol_table.set("footer", EmbedFooter(None, None))
        self.symbol_table.set("image_url", Number.null)
        self.symbol_table.set("thumbnail_url", Number.null)
        self.symbol_table.set("timestamp", Number.null)
        self.symbol_table.set("footer", Number.null)
        
        if self.value.title is not None:
            self.symbol_table.set("title", String(self.value.title))
        if self.value.description is not None:
            self.symbol_table.set("description", String(self.value.description))
        if self.value.timestamp is not None:
            self.symbol_table.set("timestamp", Number(self.value.timestamp.timestamp))
        if self.value.colour is not None:
            self.symbol_table.set("colour", Number(self.value.colour.value))
        if self.value.footer is not None:
            self.symbol_table.set("footer", EmbedFooter(self.value.footer.text, self.value.footer.icon_url))
        if self.value.image is not None:
            self.symbol_table.set("image_url", String(self.value.image.url))
        if self.value.thumbnail is not None:
            self.symbol_table.set("thumbnail_url", String(self.value.thumbnail.url))
        if self.value.author is not None:
            self.symbol_table.set("author", EmbedAuthor(self.value.author.name, self.value.author.url, self.value.author.icon_url))
        self.symbol_table.set("fields", List([
            EmbedField(field.name, field.value, field.inline) for field in self.value.fields
        ]))
            
        self.symbol_table.set("set_title", ClassFunction(self, self.set_title))
        self.symbol_table.set("set_description", ClassFunction(self, self.set_description))
        self.symbol_table.set("set_timestamp", ClassFunction(self, self.set_timestamp))
        self.symbol_table.set("set_colour", ClassFunction(self, self.set_colour))
        self.symbol_table.set("set_footer", ClassFunction(self, self.set_footer))
        self.symbol_table.set("set_image_url", ClassFunction(self, self.set_image_url))
        self.symbol_table.set("set_thumbnail_url", ClassFunction(self, self.set_thumbnail_url))
        self.symbol_table.set("set_author", ClassFunction(self, self.set_author))
        self.symbol_table.set("add_field", ClassFunction(self, self.add_field))
        
    def copy(self):
        return self

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"<Embed>"
    
    ####################################
    
    async def set_title(self, exec_ctx):
        title = exec_ctx.symbol_table.get("title")

        if not isinstance(title, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a String",
                exec_ctx
            ))

        self.value.title = title.value
        self.symbol_table.set("title", title)
        return RTResult().success(self)
    set_title.arg_names = ["title"]
    
    
    async def set_description(self, exec_ctx):
        description = exec_ctx.symbol_table.get("description")

        if not isinstance(description, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a String",
                exec_ctx
            ))
            
        self.value.description = description.value
        self.symbol_table.set("description", description)
        return RTResult().success(self)
    set_description.arg_names = ["description"]
    
    
    async def set_timestamp(self, exec_ctx):
        timestamp = exec_ctx.symbol_table.get("timestamp")

        if not isinstance(timestamp, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a Number",
                exec_ctx
            ))

        self.value.timestamp = datetime.fromtimestamp(timestamp.value)
        self.symbol_table.set("timestamp", timestamp)
        return RTResult().success(self)
    set_timestamp.arg_names = ["timestamp"]
    
    
    async def set_colour(self, exec_ctx):
        colour = exec_ctx.symbol_table.get("colour")

        if not isinstance(colour, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a Number",
                exec_ctx
            ))

        self.value.colour = colour.value
        self.symbol_table.set("colour", colour)
        return RTResult().success(self)
    set_colour.arg_names = ["colour"]
    
    
    async def set_footer(self, exec_ctx):
        text = exec_ctx.symbol_table.get("text")
        icon_url = exec_ctx.symbol_table.get("icon_url")

        if not isinstance(text, String) or text != Number.null:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a String",
                exec_ctx
            ))
        if not isinstance(icon_url, String) or icon_url != Number.null:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a String",
                exec_ctx
            ))
        
        text = None if text == Number.null else text.value
        icon_url = None if icon_url == Number.null else icon_url.value
        
        self.value.set_footer(text=text, icon_url=icon_url)
        self.symbol_table.set("footer", EmbedFooter(text, icon_url))
        return RTResult().success(self)
    set_footer.arg_names = ["text", "icon_url"]
    
    
    async def set_image_url(self, exec_ctx):
        image_url = exec_ctx.symbol_table.get("image_url")

        if not isinstance(image_url, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a String",
                exec_ctx
            ))

        self.value.set_image(url=image_url.value)
        self.symbol_table.set("image_url", image_url)
        return RTResult().success(self)
    set_image_url.arg_names = ["image_url"]
    
    
    async def set_thumbnail_url(self, exec_ctx):
        thumbnail_url = exec_ctx.symbol_table.get("thumbnail_url")

        if not isinstance(thumbnail_url, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a String",
                exec_ctx
            ))

        self.value.set_thumbnail(url=thumbnail_url.value)
        self.symbol_table.set("thumbnail_url", thumbnail_url)
        return RTResult().success(self)
    set_thumbnail_url.arg_names = ["thumbnail_url"]
    
    
    async def set_author(self, exec_ctx):
        name = exec_ctx.symbol_table.get("name")
        url = exec_ctx.symbol_table.get("url")
        icon_url = exec_ctx.symbol_table.get("icon_url")

        if not isinstance(name, String) or name != Number.null:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a String",
                exec_ctx
            ))
        if not isinstance(url, String) or url != Number.null:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a String",
                exec_ctx
            ))
        if not isinstance(icon_url, String) or icon_url != Number.null:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a String",
                exec_ctx
            ))
        
        name = None if name == Number.null else name.value
        url = None if url == Number.null else url.value
        icon_url = None if icon_url == Number.null else icon_url.value
        
        self.value.set_author(name=name, url=url, icon_url=icon_url)
        self.symbol_table.set("author", EmbedAuthor(name, url, icon_url))
        return RTResult().success(self)
    set_author.arg_names = ["name", "url", "icon_url"]
    
    
    async def add_field(self, exec_ctx):
        name = exec_ctx.symbol_table.get("name")
        value = exec_ctx.symbol_table.get("value")
        inline = exec_ctx.symbol_table.get("inline")

        if not isinstance(name, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a String",
                exec_ctx
            ))
        if not isinstance(value, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a String",
                exec_ctx
            ))
        if not isinstance(inline, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a Number",
                exec_ctx
            ))
        
        name = name.value
        value = value.value
        inline = inline.value
        
        self.value.add_field(name=name, value=value, inline=bool(inline))
        self.symbol_table.set("fields", List([
            EmbedField(field.name, field.value, field.inline) for field in self.value.fields
        ]))
        return RTResult().success(self)
    add_field.arg_names = ["name", "value", "inline"]
    
    
    
class EmbedFooter(Value):
    def __init__(self, text, icon_url):
        super().__init__()
        self.text = text
        self.icon_url = icon_url
        
        self.symbol_table.set("text", Number.null)
        self.symbol_table.set("icon_url", Number.null)
        
        if self.text is not None:
            self.symbol_table.set("text", String(self.text))
        if self.icon_url is not None:
            self.symbol_table.set("icon_url", String(self.icon_url))
        
    def copy(self):
        copy = EmbedFooter(self.text, self.icon_url)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"<EmbedFooter>"
    
    
class EmbedAuthor(Value):
    def __init__(self, name, url, icon_url):
        super().__init__()
        self.name = name
        self.url = url
        self.icon_url = icon_url
        
        self.symbol_table.set("name", Number.null)
        self.symbol_table.set("url", Number.null)
        self.symbol_table.set("icon_url", Number.null)
        
        if self.name is not None:
            self.symbol_table.set("name", String(self.name))
        if self.url is not None:
            self.symbol_table.set("url", String(self.url))
        if self.icon_url is not None:
            self.symbol_table.set("icon_url", String(self.icon_url))
        
    def copy(self):
        copy = EmbedAuthor(self.name, self.url, self.icon_url)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"<EmbedAuthor>"
    
    
    
class EmbedField(Value):
    def __init__(self, name, value, inline):
        super().__init__()
        self.name = name
        self.value = value
        self.inline = inline
        
        self.symbol_table.set("name", Number.null)
        self.symbol_table.set("value", Number.null)
        self.symbol_table.set("inline", Number.null)
        
        if self.name is not None:
            self.symbol_table.set("name", String(self.name))
        if self.value is not None:
            self.symbol_table.set("value", String(self.value))
        if self.inline is not None:
            self.symbol_table.set("inline", String(self.inline))
        
    def copy(self):
        copy = EmbedField(self.name, self.url, self.icon_url)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"<EmbedField>"