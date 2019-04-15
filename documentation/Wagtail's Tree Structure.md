# Understanding Wagtail's Tree Structure

> Wagtail is formatted in a tree-like structure. This means every page in Pipeline (section pages, article pages, and staff pages) are either parents or children.

> This relationship sounds as simple as seen in real life. A parent, or a section page, is responsible for its children, the individual articles themselves. The tabs located on the nagivation bar on the right of the Wagtail admin shows this nested structure. As you click on the tabs, you go further down the tree.

> If you add an article page or individual staff page to the wrong section, it can be moved.

## Diagram

> Hopefully this layout helps describes how the pages are connected. This is important to understand because it defines how pages are added within Pipeline. This example includes just Features and News as sections. In reality, Homepage would also have branches of Ed-Op, Staff, and any other sections _The Polytechnic_ has.

>											Homepage
>											/		\
>										   /		 \
>										  /           \
>										 /             \
>										/               \
>								  Features			 	News						
>									/ \				     / \
>								   /   \			    /   \
>							  	  /     \              /     \
>							 	 /       \            /       \
>								/         \          /         \
>							Event	   Movie	  Senate	E-Board
>							Review	   Review
