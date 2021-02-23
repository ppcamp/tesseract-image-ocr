# tesseract-image-ocr

Some codes using tesseract lib. Code inspired by [nanonets][tesseract-tuto]

At first, you'll need to install the tesseract binary:

```bash
sudo apt install tesseract-ocr
```

The code bellow it's necessary, since that the library only work as a binding to it.


## ToDo

- [ ] Fix problem with letter matching
  > For some unknowed (yet) reason, the images aren't recognized. I guess that's a problem related with large differences between the pixels, which cause a high noise.


<!-- Some links -->
[tesseract-tuto]: https://nanonets.com/blog/ocr-with-tesseract