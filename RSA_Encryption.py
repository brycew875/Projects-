class RSA:
    def __init__(self):
        self.alphabet = ".,?! \t\n\rabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.block_size = 216

    def text_to_number(self, text):
        num = 0
        for ch in text:
            num = num * len(self.alphabet) + self.alphabet.index(ch)
        return num

    def number_to_text(self, num, length):
        base = len(self.alphabet)
        text = ""
        while num > 0:
            text = self.alphabet[num % base] + text
            num //= base

        while len(text) < length:
            text = self.alphabet[0] + text
        return text

    def decrypt(self, inputfile, outputfile, private_key_file="private.txt"):
        with open(private_key_file, "r", encoding="utf-8") as f:
            n = int(f.readline().strip())
            d = int(f.readline().strip())

        with open(inputfile, "rb") as fin:
            content = fin.read().decode("utf-8")

        blocks = [block for block in content.split("$") if block]
        decrypted_blocks = []

        for block in blocks:
            clean_block = "".join(ch for ch in block if ch in self.alphabet)
            if not clean_block:
                continue

            encrypted_num = self.text_to_number(clean_block)
            plain_num = pow(encrypted_num, d, n)
            plain_block = self.number_to_text(plain_num, self.block_size)

            decrypted_blocks.append(plain_block.lstrip("."))

        final_output = "".join(decrypted_blocks)

        with open(outputfile, "w", encoding="utf-8") as fout:
            fout.write(final_output)

        print("\n--- DECRYPTED MESSAGE ---\n")
        print(final_output)
        print("\n-------------------------")
        print(f"\nSaved to {outputfile}")

if __name__ == "__main__":
    rsa = RSA()
    rsa.decrypt("BryceEncrypted.txt", "BryceDecrypted.txt")