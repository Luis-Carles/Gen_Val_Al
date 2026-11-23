from lehmer_generator import imsl_generator as imsl
# Diehard

# Generate random sample of numbers using Lehmer generator
N = 100000
seed = 12345

sample = imsl(N, seed)

print("First 10 generated numbers:")
print(sample[:10])

print("Smaple Size:", len(sample))
print("Min:", min(sample))
print("Max:", max(sample))

# Prepare the sample to be studied with Diehard
def save_sample(sample, seed, filename="imsl_sample.txt"):

    with open(filename, "w") as file:

        file.write("# IMSL Multiplicative Congruential Generator\n")
        file.write(f"# Multiplier: 16807\n")
        file.write(f"# Modulus: {2**31 - 1}\n")
        file.write(f"# Seed: {seed}\n")
        file.write(f"type: d\n")
        file.write(f"count: {len(sample)}\n")
        file.write("numbit: 32\n")

        for number in sample:
            file.write(f"{number:.15f}\n")

save_sample(sample, seed)

