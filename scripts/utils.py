def load_template():
    with open("template/template.html", "r", encoding="utf-8") as file:
        template = file.read()
        template = template.replace("{", "{{").replace("}", "}}")
        template = template.replace("{{channel_name}}", "{channel_name}")
        template = template.replace("{{channelID}}", "{channelID}")
        template = template.replace("{{subscriber_count}}", "{subscriber_count}")
        template = template.replace("{{video_cards}}", "{video_cards}")
        template = template.replace("{{last_video_cards}}", "{last_video_cards}")
        template = template.replace("{{thumbnail}}", "{thumbnail}")
        template = template.replace("{{subscriber_count}}", "{subscriber_count}")
        template = template.replace("{{description}}", "{description}")
        template = template.replace("{{video_count}}", "{video_count}")
        template = template.replace("{{views_count}}", "{views_count}")
        return template
