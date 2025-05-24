{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShell.${system} = pkgs.mkShell {
        packages = with pkgs; [
	  pyright
	  ruff
     gtk3
          shared-mime-info
          (python312.withPackages (
            python-pkgs: with python-pkgs; [
              pandas
              openpyxl
              xlrd
              tkinter
              customtkinter
              pyinstaller
              jupyter-core
              ipython
	      notebook
            ]
          ))
        ];
        shellHook = ''
          exec zsh
        '';
      };
    };
}
