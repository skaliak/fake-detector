import fake_detector, data_layer

def main():
    print("test_harness.py")
    detector = fake_detector.FakeDetector(data_layer.HardCodedDataAccess())
    print(detector.get_r4r_subreddits())

if __name__ == "__main__":
    main()