import os 
cmd = "node abiEnc.js 0x2D737a24725A02F6C95FE51f8B83029759110b0F  SimpleStorage 2 1000 true"
output_stream = os.popen(cmd)
print(output_stream.read())
encoding = os.popen(cmd).read()

