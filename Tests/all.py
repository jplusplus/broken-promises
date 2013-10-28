import unittest

if __name__ == "__main__":
	tests = unittest.TestLoader().discover("collector", "*.py")
	unittest.TextTestRunner(verbosity=2).run(tests)

# EOF
