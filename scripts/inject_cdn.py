"""Inject CDN links for KaTeX and Mermaid into the EduSphere PWA."""
with open('static/index.html', 'rb') as f:
    content = f.read().decode('utf-8')

if 'katex' in content:
    print('KaTeX already present, skipping.')
else:
    # Find the closing </title> + CRLF + <style> sequence
    marker_candidates = ['</title>\r\n<style>', '</title>\n<style>']
    marker = None
    for m in marker_candidates:
        if m in content:
            marker = m
            break
    if marker is None:
        print('ERROR: Could not find </title>+<style> marker')
        print(repr(content[485:530]))
    else:
        cdn = (
            '<!-- KaTeX math rendering (grades 3+) -->\n'
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css" crossorigin="anonymous">\n'
            '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js" crossorigin="anonymous"></script>\n'
            '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/contrib/auto-render.min.js" crossorigin="anonymous" onload="window._katexLoaded=true"></script>\n'
            '<!-- Mermaid.js: diagram rendering in chat -->\n'
            '<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js" defer></script>\n'
        )
        sep = '\r\n' if '\r\n' in marker else '\n'
        replacement = f'</title>{sep}{cdn}<style>'
        content = content.replace(marker, replacement, 1)
        with open('static/index.html', 'wb') as f:
            f.write(content.encode('utf-8'))
        print('SUCCESS: KaTeX + Mermaid CDN injected into index.html')
