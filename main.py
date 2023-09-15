import RPi.GPIO as GPIO
import asyncio
from asyncua import ua, uamethod, Server

R = False
G = False
B = False


async def main():
    try:
        server = Server()
        await server.init()
        server.set_endpoint("opc.tcp://10.4.1.213:4840")
        server.set_server_name("Serveur LED XX")
        server.set_security_policy(
            [
                ua.SecurityPolicyType.NoSecurity,
                ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
                ua.SecurityPolicyType.Basic256Sha256_Sign,
            ]
        )

        uri = "http://monURI"
        idx = await server.register_namespace(uri)

        machine_node = await server.nodes.objects.add_object(idx, "machine")

        GPIO.setmode(GPIO.BCM)

        async def async_toggle_red():
            global R
            R = not R
            GPIO.setup(21, GPIO.OUT)
            GPIO.output(21, GPIO.HIGH if not R else GPIO.LOW)

        async def async_toggle_green():
            global G
            G = not G
            GPIO.setup(20, GPIO.OUT)
            GPIO.output(20, GPIO.HIGH if not G else GPIO.LOW)

        async def async_toggle_blue():
            global B
            B = not B
            GPIO.setup(16, GPIO.OUT)
            GPIO.output(16, GPIO.HIGH if not B else GPIO.LOW)

        @uamethod
        def toggle_red(parent_node_id):
            asyncio.run(async_toggle_red())

        @uamethod
        def toggle_green(parent_node_id):
            asyncio.run(async_toggle_green())

        @uamethod
        def toggle_blue(parent_node_id):
            asyncio.run(async_toggle_blue())

        toggle_red_node = await machine_node.add_method(idx, "toggleRed", toggle_red, [], [],)
        toggle_green_node = await machine_node.add_method(idx, "toggleGreen", toggle_green, [], [],)
        toggle_blue_node = await machine_node.add_method(idx, "toggleBlue", toggle_blue, [], [],)

        async with server:
            while True:
                await asyncio.sleep(0.1)
    finally:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21, GPIO.OUT)
        GPIO.output(21, GPIO.HIGH)
        GPIO.setup(20, GPIO.OUT)
        GPIO.output(20, GPIO.HIGH)
        GPIO.setup(16, GPIO.OUT)
        GPIO.output(16, GPIO.HIGH)
        GPIO.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
