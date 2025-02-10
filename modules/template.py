def load_template():
    with open("templates/template.html", "r", encoding="utf-8") as file:
        template = file.read()
        template = template.replace("{", "{{").replace("}", "}}")
        template = template.replace("{{video_cards}}", "{video_cards}")
        template = template.replace("{{last_video_cards}}", "{last_video_cards}")
        template = template.replace("{{channel_info}}", "{channel_info}")
        return template

def load_main():
    with open("templates/template_main.html", "r", encoding="utf-8") as file:
        template = file.read()
        template = template.replace("{", "{{").replace("}", "}}")
        template = template.replace("{{container}}", "{container}")
        return template
