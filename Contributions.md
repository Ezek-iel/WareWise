## Contributing to Warewise Project

### Getting Started

1. Fork the repository on GitHub.

2. Clone the forked repository to your local machine.

   ```bash
   git clone https://github.com/Ezek-iel/WareWise.git
   ```

3. Create the virtual environment.

   - On Windows:

   ```shell
   py -m venv .venv
   ```

   ```shell
   .venv\Scripts\activate
   ```

   - On macOS/Linux:
   
   ```shell
   python3 -m venv .venv
   ```

   ```bash
   source venv/bin/activate
   ```

4. Install all dependacies

   ```shell
   pip intall -r requirements.txt
   ```

### Coding Standards

- We used imperative python style instead of the `.kv` style
- Use camelCase for all variable names.

   ```python
   settingsCard = MDCard()
   ```

### Making Changes

1. Create a new branch for your changes.

   ```bash
   git checkout -b feature-name
   ```

2. Make your changes and commit them.

   ```bash
   git add .
   git commit -m "Your descriptive commit message"
   ```

3. Push the changes to your fork on GitHub.

   ```bash
   git push origin feature-name
   ```

4. Create a pull request on the original repository.

### Thank You

Thanks for contributing to WareWise! Your efforts make the project better for everyone. 🚀

