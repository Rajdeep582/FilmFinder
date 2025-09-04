mkdir -p ~/.streamlit/

# shellcheck disable=SC2028
echo "\
[server]\n\
headless = true\n\
port = \$PORT\n\
enableCORS = true\n\
\n\
" > ~/.streamlit/config.toml
