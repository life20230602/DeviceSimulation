def inject_device_info(window, device):
    # 覆盖 UA
    window.evaluate_js(
        f'navigator.__defineGetter__("userAgent", function() {{ return "{device["ua"]}"; }});'
    )
    # 覆盖 navigator 属性
    for key, value in device["navigator"].items():
        js_value = f'"{value}"' if isinstance(value, str) else str(value)
        window.evaluate_js(
            f'Object.defineProperty(navigator, "{key}", {{ get: function() {{ return {js_value}; }} }});'
        )
    # 覆盖 screen 属性
    for key, value in device["screen"].items():
        window.evaluate_js(
            f'Object.defineProperty(screen, "{key}", {{ get: function() {{ return {value}; }} }});'
        )
    