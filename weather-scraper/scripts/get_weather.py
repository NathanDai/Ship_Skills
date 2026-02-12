import httpx


class WeatherSkill:
    """查询指定城市当前天气的技能"""

    name = "weather"
    description = "查询指定城市当前天气"

    parameters = {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "城市名称，例如 Beijing 或 New York",
            }
        },
        "required": ["city"],
    }

    async def execute(self, city: str) -> dict:
        """
        执行天气查询

        Args:
            city (str): 城市名称

        Returns:
            dict: 包含天气信息的字典，或者包含错误信息的字典
        """
        try:
            url = f"https://wttr.in/{city}?format=j1"
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=30.0)
                response.raise_for_status()

                data = response.json()
                current = data["current_condition"][0]

                return {
                    "city": city,
                    "temperature": current["temp_C"] + "°C",
                    "weather": current["weatherDesc"][0]["value"],
                    "humidity": current["humidity"] + "%",
                    "wind": current["windspeedKmph"] + " km/h",
                }

        except httpx.HTTPStatusError as e:
            return {"error": f"查询失败: HTTP {e.response.status_code}"}
        except httpx.RequestError as e:
            return {"error": f"网络请求失败: {str(e)}"}
        except Exception as e:
            return {"error": f"未知错误: {str(e)}"}


if __name__ == "__main__":
    import argparse
    import asyncio
    import json

    async def main():
        parser = argparse.ArgumentParser(description="查询特定城市的天气。")
        parser.add_argument("city", type=str, help="要查询的城市名称")
        args = parser.parse_args()

        skill = WeatherSkill()
        result = await skill.execute(args.city)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    asyncio.run(main())
