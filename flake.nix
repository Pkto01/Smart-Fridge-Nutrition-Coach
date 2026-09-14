{
  description = "python smart fridge";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs;[
          python314
          direnv
          nix-direnv
        ];
        shellHook = ''
         export PS1="(dev shell python) \[\e[38;5;75m\]\u@\h \[\e[38;5;113m\]\w \[\e[38;5;189m\]\$ \[\e[0m\]"
         echo "setting up python env..."
         python3 -m venv venv
         source ./venv/bin/activate

         pip install fastapi pydantic fastapi[standard] requests
        '';
      };
    };
}