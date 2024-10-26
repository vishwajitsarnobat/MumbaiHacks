targeting = json_str["campaign_data"]
        # (status, details) = generate_ad_content(
        #     targeting["locations"],
        #     "general public",
        #     input_json["languages"],
        #     input_json["prompt"],
        # )
        # # {"language":([title],[description],image)}
        # if status:
        #     for language in details:
        #         input_json["campaigns"]["ad"]["headlines"] = []
        #         input_json["campaigns"]["ad"]["descriptions"][i] = []
        #         input_json["campaigns"]["ad"]["images"][0] = details[language][2]
        #         for i in len(details[language][0]):
        #             input_json["campaigns"]["ad"]["headlines"].push(
        #                 details[language][0][i]
        #             )
        #             input_json["campaigns"]["ad"]["descriptions"][i].push(
        #                 details[language][1][i]
        #             )