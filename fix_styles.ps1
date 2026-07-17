$cssToAdd = "
/* --- Education Hub Styles --- */
.module-accordion summary {
    padding: 1.5rem;
    font-family: var(--heading-font);
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--navy);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
    list-style: none;
    transition: background-color 0.2s ease;
}
.module-accordion summary:hover {
    background-color: var(--stone);
}
.module-accordion summary::-webkit-details-marker {
    display: none;
}
.caret {
    color: var(--gold);
    font-size: 1.5rem;
    transition: transform 0.3s ease;
}
.module-accordion[open] .caret {
    transform: rotate(180deg);
}
.article-link {
    color: var(--navy);
    text-decoration: none;
    font-size: 1.05rem;
    font-weight: 600;
    display: block;
    padding: 0.75rem 1rem;
    border-left: 3px solid transparent;
    transition: all 0.2s ease;
}
.article-link:hover {
    border-left: 3px solid var(--gold);
    color: var(--gold);
    background-color: var(--white);
}

/* --- Article Styles --- */
.article-container { max-width: 800px; margin: 4rem auto; padding: 3rem; background: var(--white); border-radius: 12px; box-shadow: 0 10px 30px rgba(11,29,58,0.08), 0 1px 8px rgba(11,29,58,0.03); border-top: 5px solid var(--gold); }
.article-content { font-family: var(--body-font); color: var(--navy); }
.article-content h1 { color: var(--navy); margin-bottom: 0.5rem; font-size: 2.5rem; font-family: var(--heading-font); font-weight: 700; line-height: 1.2; letter-spacing: -0.5px; }
.article-content h2, .article-content h3, .article-content h4 { color: var(--navy); margin-top: 2.5rem; margin-bottom: 1.2rem; font-family: var(--heading-font); font-weight: 700; }
.article-content p { line-height: 1.8; margin-bottom: 1.8rem; font-size: 1.15rem; color: var(--navy); }
.article-content ul, .article-content ol { margin-bottom: 1.8rem; padding-left: 2rem; color: var(--navy); }
.article-content li { margin-bottom: 0.8rem; line-height: 1.7; font-size: 1.15rem; color: var(--navy); }
.article-content table { width: 100%; border-collapse: collapse; margin-bottom: 2rem; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(11,29,58,0.05); }
.article-content th, .article-content td { border: 1px solid var(--stone); padding: 1rem; text-align: left; color: var(--navy); }
.article-content th { background-color: var(--navy); color: var(--white); font-weight: 600; text-transform: uppercase; font-size: 0.9rem; letter-spacing: 1px; }
.article-content tr:nth-child(even) { background-color: var(--cream); }
.apply-it, .further-reading, .article-disclaimer { background-color: var(--stone); border: 1px solid var(--gold); padding: 2rem; margin: 3rem 0; border-radius: 8px; position: relative; }
.apply-it p, .further-reading p { color: var(--navy); }
.apply-it p:last-child, .further-reading p:last-child { margin-bottom: 0; }
.apply-it p:first-child, .further-reading p:first-child { margin-bottom: 0.5rem; }
.apply-it p:first-child strong, .further-reading p:first-child strong { color: var(--gold); text-transform: uppercase; letter-spacing: 1px; font-size: 0.9rem; }
.breadcrumb { margin-bottom: 3rem; font-size: 0.95rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; }
.breadcrumb a { color: var(--gold); text-decoration: none; display: inline-flex; align-items: center; transition: all 0.2s ease; }
.breadcrumb a:hover { color: var(--navy); transform: translateX(-5px); }
.article-crosslink { color: var(--gold); font-weight: 400; text-decoration: none; border-bottom: 2px solid var(--gold); transition: all 0.2s ease; }
.article-crosslink:hover { background-color: transparent; border-bottom-color: var(--navy); color: var(--navy); }
.article-disclaimer p { margin-bottom: 0; color: var(--navy); font-size: 0.9rem; line-height: 1.6; text-align: justify; }
"

Add-Content -Path "style.css" -Value $cssToAdd
Write-Host "Appended styles to style.css"

$files = Get-ChildItem -Path . -Filter "*.html"
foreach ($file in $files) {
    if ($file.Name -match "^article-" -or $file.Name -eq "education.html") {
        $content = Get-Content -Raw -Path $file.FullName
        # Replace the entire <style> block
        $newContent = $content -replace "(?s)<style>.*?</style>\s*", ""
        Set-Content -Path $file.FullName -Value $newContent
        Write-Host "Removed <style> from $($file.Name)"
    }
}
