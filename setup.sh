SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
export PATH=$PATH:${SHELL_FOLDER}"/phonetisaurus/bin":${SHELL_FOLDER}"/phonetisaurus/scripts"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${SHELL_FOLDER}"/phonetisaurus/lib"